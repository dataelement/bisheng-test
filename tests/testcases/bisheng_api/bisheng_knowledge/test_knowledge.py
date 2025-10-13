# -*- coding: utf-8 -*-
# @Time    : 2025/8/19 15:20
# @Author  : sara
# @Email   : your-email@example.com
from datetime import datetime
import os
import pytest
import allure

from tests.confdata import CONFDATA
from tests.utils.http_utils import prepare_data
from tests.utils.log_util import LogUtil
from tests.utils.res_check import  compare_res_code


@allure.epic('API服务接口自动化测试')
@allure.story('知识库创建接口结果')
class TestBISHENGKNOWLAGE:
    @pytest.mark.parametrize("args", CONFDATA.knowledge_cases())
    def test_knowledge(self, args):
        print("用例ID:{}".format(args[0]['id']))
        print("用例名称:{}".format(args[0]['case_name']))
        # cookies = get_cookies()

        # bisheng_ep = os.environ.get('TEST_BISHENG_EP')
        bisheng_ep = os.environ.get("TEST_BISHENG_EP")
        print("bisheng_ep:{}".format(bisheng_ep))
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        args[0]['body']['name'] = args[0]['body']['name'] + current_date
        # 发起请求
        res = prepare_data(args, bisheng_ep)

        # log_text = "case_name: %s" % (case_name)
        # LogUit.log_info(log_text)

        # compare
        status_report = "\n"
        status_report = compare_res_code(res, args, status_report)
        if status_report is None:
            status_report = str(status_report)
        LogUtil().info(status_report)
        with allure.step("接口返回：%s" % status_report):
            pass
