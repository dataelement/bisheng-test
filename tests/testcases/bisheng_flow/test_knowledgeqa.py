# flake8: noqa
import allure
import pytest
import os
from tests.confdata import CONFDATA

from tests.utils.log_util import LogUtil
from tests.utils.res_check import compare_res_konwlages
from tests.utils.yaml_util import FromYaml2Json
from tests.utils.http_utils import prepare_dataqa


@allure.epic('API服务接口自动化测试')
@allure.feature('测试环境端口3002')
@allure.story('通用识别模型自动化接口结果')
class TestKNOWLAGEQA:
    @pytest.mark.parametrize("args", CONFDATA.knowledgeqa_cases())
    def test_knowlages(self, args):
        print("用例ID:{}".format(args[0]['id']))
        print("用例名称:{}".format(args[0]['case_name']))

        flowid = os.environ.get('FLOW_ID')
        bisheng_ep = os.environ.get('TEST_BISHENG_EP')
        res = prepare_dataqa(args, bisheng_ep, flowid)

        # log_text = "case_name: %s" % (case_name)
        # LogUit.log_info(log_text)

        # compare
        status_report = "\n"
        status_report = compare_res_konwlages(res, args, status_report)
        if status_report is None:
            status_report = str(status_report)
        LogUtil().info(status_report)
        with allure.step("接口返回：%s" % (status_report)):
            pass

