# flake8: noqa
import pytest
import allure

from tests.utils.log_util import LogUtil
from tests.utils.res_check import compare_res_konwlages


@allure.epic('bisheng接口自动化测试')
@allure.feature('bisheng服务端口，端口3002')
@allure.story('大模型自动化接口结果')
class TestBISHENGLargemodel:
    @pytest.mark.parametrize("args", pytest.lazy_fixture('knowledge_cases'))
    def test_largemodel(self, args):
        # for args in data_item:
        # 打印用例ID和名称到报告中显示
        print("用例ID:{}".format(args['id']))
        print("用例名称:{}".format(args['case_name']))
        # print("用例图片:{}".format(args['body']['image']))

        bisheng_ep = os.environ.get('TEST_BISHENG_EP')
        res = prepare_data(args, TEST_HOST)

        # log_text = "case_name：%s" % (case_name)
        # LogUtil().info(log_text)

        # compare
        status_report = "\n"
        status_report = compare_res_konwlages(res, args, status_report)
        if status_report is None:
            status_report = str(status_report)
        LogUtil().info(status_report)
        with allure.step("接口返回：%s" % (status_report)):
            pass
