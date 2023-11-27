# flake8: noqa
"""
@Time ： 2023/10/27 17:03
@Auth ： Sara
@File ：test_unstructuredLoaderV0.py
@IDE ：PyCharm
"""

import pytest
import allure

from tests.utils.log_util import LogUtil
from tests.utils.res_check import compare_res
from tests.utils.http_utils import unstructuredLoaderv0


# @allure.epic('bisheng接口自动化测试')
# @allure.feature('bisheng服务端口，端口3002')
@allure.story('UnstructuredLoaderV0自动化接口结果')
class TestUnstructuredLoaderV0:
    @pytest.mark.parametrize("args", pytest.lazy_fixture('uns_cases'))
    def test_unstructuredLoaderV0(self, args):
        # for args in data_item:
        # 打印用例ID和名称到报告中显示
        print("用例ID:{}".format(args['id']))
        print("用例名称:{}".format(args['case_name']))
        # print("用例图片:{}".format(args['body']['image']))
        # b64_data = base64.b64encode(open(filename, "rb").read()).decode()
        # inp = dict(
        #     filename=os.path.basename(filename),
        #     b64_data=[b64_data],
        #     mode="text")
        # resp = requests.post(url, json=inp).json()

        uns_ep = os.environ.get('TEST_UNSTRUCTURED_EP')
        res = unstructuredLoaderv0(args, uns_ep)

        # log_text = "case_name：%s" % (case_name)
        # LogUtil().info(log_text)

        # compare
        status_report = "\n"
        status_report = compare_res(res, args, status_report)
        if status_report is None:
            status_report = str(status_report)
        LogUtil().info(status_report)
        with allure.step("接口返回：%s" % (status_report)):
            pass
