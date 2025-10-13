# -*- encoding: utf-8 -*-
'''
@File    :   test_knowledgeqa.py
@Time    :   2024/03/04 16:22:00
@Author  :   Sara 
@Version :   1.0
'''
# flake8: noqa
import os
import pytest
import allure
from tests.confdata import CONFDATA

from tests.utils.log_util import LogUtil
from tests.utils.res_check import compare_res
from tests.utils.http_utils import prepare_data


@allure.epic('API服务接口自动化测试')
@allure.story('知识库问答场景')
class TestBISHENGKNOWLAGEQA:
    @pytest.mark.parametrize("args", CONFDATA.knowledgeqa_cases())
    def test_knowledgeqa(self, args):
        print("用例ID:{}".format(args[0]['id']))
        print("用例名称:{}".format(args[0]['case_name']))
        bisheng_ep = os.environ.get('TEST_BISHENG_EP')
        # current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # args[0]['body']['name'] = args[0]['body']['name'] + current_date 
        res = prepare_data(args, bisheng_ep)

        # log_text = "case_name: %s" % (case_name)
        # LogUit.log_info(log_text)

        # compare
        status_report = "\n"
        # status_report = compare_res(res, args, status_report)
        if status_report is None:
            status_report = str(status_report)
        LogUtil().info(status_report)
        with allure.step("接口返回：%s" % (status_report)):
            pass
