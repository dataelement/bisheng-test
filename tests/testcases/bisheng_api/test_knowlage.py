# flake8: noqa
import pytest
import allure

from tests.utils.log_util import LogUtil
from tests.utils.res_check import compare_res
from tests.utils.http_utils import prepare_data_knowlagecreate


@allure.epic('API服务接口自动化测试')
@allure.feature('端口3002')
@allure.story('通用识别模型自动化接口结果')
class TestBISHENGKNOWLAGE:
    @pytest.mark.parametrize("args", pytest.lazy_fixture('knowledge_cases'))
    def test_knowlages(self, args):
        print("用例ID:{}".format(args['id']))
        print("用例名称:{}".format(args['case_name']))
        bisheng_ep = os.environ.get('TEST_BISHENG_EP')
        res = prepare_data_knowlagecreate(args, bisheng_ep)

        # log_text = "case_name: %s" % (case_name)
        # LogUit.log_info(log_text)

        # compare
        status_report = "\n"
        status_report = compare_res(res, args, status_report)
        if status_report is None:
            status_report = str(status_report)
        LogUtil().info(status_report)
        with allure.step("接口返回：%s" % (status_report)):
            pass
