# flake8: noqa
import argparse
import os
import pytest
import sys
import subprocess
from pathlib import Path
from multiprocessing import cpu_count


def _test_python(args, default_dir="tests/testcases"):
    print("\nRunning Python tests...\n")

    curr_dir = Path(__file__).parent.resolve()
    test_dir = curr_dir / default_dir
    pytest_args = []

    # 处理单个测试文件
    if args.files:
        for f in args.files:
            file_path = Path(f)
            # 如果是相对路径，尝试在测试目录中查找
            if not file_path.is_absolute():
                file_path = test_dir / file_path

            # 自动补全文件名（仅对文件名部分添加 test_ 和 .py）
            if not file_path.name.startswith("test_"):
                file_path = file_path.with_name(f"test_{file_path.name}")
            if not file_path.suffix == ".py":
                file_path = file_path.with_suffix(".py")

            if file_path.exists():
                pytest_args.append(str(file_path))
            else:
                raise FileNotFoundError(f"Test file not found: {file_path}")
    else:
        # 默认运行整个测试目录
        pytest_args.append(str(test_dir))

    # ✅ 添加 allure 报告生成目录
    allure_dir = "./allure-results"
    pytest_args += ["--alluredir", allure_dir]

    # 添加通用参数
    if getattr(args, "verbose", False):
        pytest_args += ["-v"]
    if getattr(args, "rerun", None):
        pytest_args += ["--reruns", str(args.rerun)]

    # 添加可选参数（兼容属性不存在的情况）
    optional_args = {
        "coverage": ["--cov-branch", "--cov=."],  # 默认当前目录
        "cov_append": ["--cov-append"],
        "keys": ["-k", args.keys],
        "marks": ["-m", args.marks],
        "failed_first": ["--failed-first"],
        "fail_fast": ["--exitfirst"],
        "timeout": [
            "--durations=15",
            f"--timeout={args.timeout}"
        ] if getattr(args, "timeout", 0) > 0 else None
    }

    for attr, arg_list in optional_args.items():
        if getattr(args, attr, None) and arg_list:
            pytest_args += arg_list

    # 设置线程数
    try:
        threads = min(8, cpu_count())
    except NotImplementedError:
        threads = 2
    threads = getattr(args, "threads", None) or os.environ.get("BISHENG_TEST_THREADS", threads)
    print(f"Starting {threads} testing thread(s)...")

    if getattr(args, "show_output", False):
        pytest_args += ["-s"]
        if int(threads) > 1:
            print("Warning: -s option may not work with multiple threads (pytest-xdist limitation)")
    elif int(threads) > 1:
        pytest_args += ["-n", str(threads)]

    # 运行 pytest 并返回退出码
    return int(pytest.main(pytest_args))

# @pytest.mark.skip(reason="This is not a pytest test function, it's the main runner")
def test():
    """Run the tests and auto-generate Allure report"""
    parser = argparse.ArgumentParser(description="Run bisheng python test")
    parser.add_argument("files", nargs="*", help='Test name(s) to be run, e.g. "cli"')
    parser.add_argument(
        "-c",
        "--cpp",
        dest="cpp",
        default=False,
        action="store_true",
        help="Only run the C++ tests",
    )
    parser.add_argument(
        "-s",
        "--show",
        dest="show_output",
        action="store_true",
        help="Show output (do not capture)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Run with verbose outputs",
    )
    parser.add_argument(
        "-r",
        "--rerun",
        required=False,
        default=None,
        dest="rerun",
        type=str,
        help="Rerun failed tests for given times",
    )
    parser.add_argument(
        "-k",
        "--keys",
        required=False,
        default=None,
        dest="keys",
        type=str,
        help="Only run tests that match the keys",
    )
    parser.add_argument(
        "-m",
        "--marks",
        required=False,
        default=None,
        dest="marks",
        type=str,
        help="Only run tests with specific marks",
    )
    parser.add_argument(
        "-f",
        "--failed-first",
        required=False,
        default=None,
        dest="failed_first",
        action="store_true",
        help="Run the previously failed test first",
    )
    parser.add_argument(
        "-x",
        "--fail-fast",
        required=False,
        default=None,
        dest="fail_fast",
        action="store_true",
        help="Exit instantly on the first failed test",
    )
    parser.add_argument(
        "-C",
        "--coverage",
        required=False,
        default=None,
        dest="coverage",
        action="store_true",
        help="Run tests and record the coverage result",
    )
    parser.add_argument(
        "-T",
        "--timeout",
        required=False,
        default=600,
        type=int,
        dest="timeout",
        help="Per test timeout (only apply to python tests)",
    )
    parser.add_argument(
        "-A",
        "--cov-append",
        required=False,
        default=None,
        dest="cov_append",
        action="store_true",
        help="Append coverage result to existing one instead of overriding it",
    )
    parser.add_argument(
        "-t",
        "--threads",
        required=False,
        default=None,
        dest="threads",
        type=str,
        help="Custom number of threads for parallel testing",
    )

    run_count = 1
    args = parser.parse_args()
    print(args)

    ret = 0
    for _ in range(run_count):
        ret = _test_python(args)
        if ret == 5:
            ret = 0  # 没有收集到测试，也认为是OK

        # 打印友好的总结信息，不调用 sys.exit
        if ret == 0:
            print("\n✅ 执行完毕：所有测试通过！")
        elif ret == 1:
            print("\n⚠️  执行完毕：有测试失败！（但脚本正常结束，不报错）")
        elif ret == 4:
            print("\n⚠️  执行完毕：没有收集到任何测试用例（检查文件/路径是否正确）")
        else:
            print(f"\n⚠️  执行完毕：测试返回未知状态码 ret={ret}")

    # =============================
    # ✅ 自动生成并打开 Allure 报告
    # =============================
    allure_results_dir = "./allure-results"
    allure_report_dir = "./allure-report"

    if not os.path.exists(allure_results_dir):
        print(f"⚠️  警告：未找到 Allure 数据目录 '{allure_results_dir}'，跳过生成报告。")
    else:
        print("🔍 正在生成 Allure 测试报告...")
        try:
            # 生成 Allure 报告
            subprocess.run([
                "allure", "generate",
                allure_results_dir,
                "-o", allure_report_dir,
                "--clean"
            ], check=True)
            print(f"✅ Allure 报告已生成，路径：{os.path.abspath(allure_report_dir)}")
        except subprocess.CalledProcessError as e:
            print(f"❌ 生成 Allure 报告失败: {e}")
        except FileNotFoundError:
            print("❌ 未找到 `allure` 命令。请确保已安装 Allure CLI 并添加到 PATH。")

        # 检测是否为 PyCharm 环境，避免重复打开
        is_pycharm = "PYCHARM_HOSTED" in os.environ or "PYCHARM" in os.environ.get("TERM", "")

        if not is_pycharm:
            try:
                print("🔗 正在打开 Allure 报告...")
                subprocess.Popen(["allure", "open", allure_report_dir])
            except Exception as e:
                print(f"⚠️ 打开报告失败: {e}")
        else:
            print("📋 PyCharm 环境 detected，跳过自动打开报告")
            print(f"   请手动运行: allure open {allure_report_dir}")

    # ✅ 确保脚本退出，返回 pytest 的退出码
    print(f"🔚 脚本执行完成，退出码: {ret}")
    sys.exit(ret)


if __name__ == "__main__":
    test()