import subprocess as sp
import os

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import starlette.status as status
import gradio as gr

app = FastAPI()


def run_test(input_cmd, params, sub_module):
    env = os.environ
    for kv in params.split('\n'):
        k, v = kv.strip().split('=', 1)
        env[k] = v

    test_module = sub_module if sub_module else "./tests"
    # test_module = "./tests/testcases/bisheng_uns"

    allure_set = "--alluredir /app/data/allure-results"
    pytest_args = "-p no:warnings -s -v"
    if input_cmd:
        command = f"{input_cmd} {allure_set}"       
    else:
        command = f"python3 -m pytest {pytest_args} {test_module} {allure_set}"

    # assert "pytest" in command, f'command is unsupported'
    try:
        status = sp.check_output(command.split(), env=env).decode("utf-8")
        return status
    except Exception as e:
        return f"Exception: {str(e)}"

def gen_report():
    command = """
      allure generate /app/data/allure-results 
      -o /app/data/default-reports --clean
    """
    _norm = lambda x: ' '.join([v.strip() for v in x.strip().split('\n')])
    command = _norm(command)
    try:
        status = sp.check_output(command.strip().split()).decode("utf-8") 
        return status
    except Exception as e:
        return f"Exception: {str(e)}"

def reset():
    cmd = "kill -9 $(ps aux |grep pytest | grep -v 'grep' | awk '{print $2}')"
    os.system(cmd)
    return None

# Bisheng Test Manager
with gr.Blocks() as demo:
    gr.Markdown("# Bisheng Test Manager")
    gr.Markdown("Developed by DataElem Inc.")

    _norm_str = lambda x: '\n'.join([v.strip() for v in x.strip().split('\n')])
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## Bisheng Full Test")
            default_params = """
                TEST_BISHENG_EP=192.168.106.120:3002
                TEST_UNSTRUCTURED_EP=192.168.106.12:20001
                TEST_RT_EP=192.168.106.12:19001
                TEST_RT_GPU=0
                TEST_RT_LLM_GPU=0,1
            """

            default_params = _norm_str(default_params)
            params = gr.Textbox(value=default_params, label="参数设置", lines=5)
            cmd = gr.Textbox(label="运行命令", lines=2)
            sub_module = gr.Textbox(label="测试模块", lines=2)
                     
            gr.Markdown("### 运行结果")
            result1 = gr.Textbox(label="result", lines=1)

            btn1 = gr.Button("运行")
            btn1.click(run_test, [cmd, params, sub_module], result1)

            btn2 = gr.Button("重置")
            btn2.click(lambda : (None), [], [result1])

        with gr.Column(scale=1):
            gr.Markdown("## Bisheng Allure Gen & See")
            gr.Markdown("### 运行结果")
            result2 = gr.Textbox(label="result", lines=1)
            btn3 = gr.Button("运行")
            gr.Markdown("[See Allure Report](/allure)")
            btn3.click(gen_report, [], result2)
            btn4 = gr.Button("重置")
            btn4.click(lambda : (None), [], [result2])


app = gr.mount_gradio_app(app, demo, path="/")

