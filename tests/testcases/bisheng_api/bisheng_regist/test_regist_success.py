#  flake8: noqa
"""
@Time ： 2023/9/26 17:29
@Auth ： Sara
@File ：test_regist_success.py
@IDE ：PyCharm
"""
import base64
from datetime import datetime
import os
import time

import pytest
import allure
import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from tests.confdata import CONFDATA

from tests.utils.log_util import LogUtil
from tests.utils.http_utils import  prepare_data
from tests.utils.res_check import compare_res_code


class TestBiShengRegist:

    def setup_method(self):
        """每个测试方法前的初始化"""
        self.session = requests.Session()
        self.public_key = None
        self.base_url = os.environ.get('TEST_BISHENG_EP', '')


    def get_public_key(self):
        """获取RSA公钥"""
        url = f"{self.base_url}/api/v1/user/public_key"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()["data"]["public_key"]

    @staticmethod
    def rsa_encrypt(password, public_key):
        """RSA加密密码"""
        rsa_key = RSA.import_key(public_key)
        cipher = PKCS1_v1_5.new(rsa_key)
        encrypted = cipher.encrypt(password.encode())
        return base64.b64encode(encrypted).decode()

    @pytest.mark.parametrize("args", CONFDATA.regist_cases())
    def test_regist(self, args):
        # datetime = time.time()

        # for args in data_item:
        # 打印用例ID和名称到报告中显示
        print("用例ID:{}".format(args[0]['id']))
        print("用例名称:{}".format(args[0]['case_name']))
        bisheng_ep = os.environ.get('TEST_BISHENG_EP')
        # 加密密码
        encrypted_pwd = self.rsa_encrypt(args[0]['body']['password'],public_key=self.get_public_key())
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        args[0]['body']['user_name'] = args[0]['body']['user_name'] + current_date
        args[0]['body']['password'] = encrypted_pwd
        #发起请求
        res = prepare_data(args, bisheng_ep)


        # compare
        status_report = "\n"
        status_report = compare_res_code(res, args, status_report)
        if status_report is None:
            status_report = str(status_report)
        LogUtil().info(status_report)
        with allure.step("接口返回：%s" % status_report):
            pass