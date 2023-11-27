#  flake8: noqa
"""
@Time ： 2023/9/26 17:29
@Auth ： Sara
@File ：test_regist_success.py
@IDE ：PyCharm
"""
import time

import pytest
import allure

from tests.utils.log_util import LogUtil
from tests.utils.res_check import compare_res
from tests.utils.http_utils import prepare_data, prepare_data_regist


class TestBiShengRegist:
    @pytest.mark.parametrize("args", pytest.lazy_fixture('regist_cases'))
    def test_regist(self, args):
        # datetime = time.time()

        # for args in data_item:
        # 打印用例ID和名称到报告中显示
        print("用例ID:{}".format(args['id']))
        print("用例名称:{}".format(args['case_name']))

        bisheng_ep = os.environ.get('TEST_BISHENG_EP')
        res = prepare_data_regist(args, TEST_HOST)
        print(res)

        # log_text = "case_name：%s" % (case_name)
        # LogUtil().info(log_text)
        # res_login = prepare_data(res., TEST_HOST, TEST_PORT)


        # compare
        status_report = "\n"
        status_report = compare_res(res, args, status_report)
        if status_report is None:
            status_report = str(status_report)
        LogUtil().info(status_report)
        with allure.step("接口返回：%s" % (status_report)):
            pass
