# flake8: noqa
import base64
import os

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

import pytest
import allure
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from tests.confdata import CONFDATA
from tests.utils.log_util import LogUtil


class SessionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_session()
        return cls._instance

    def _init_session(self):
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def get_session(self):
        return self.session


@allure.epic('API服务接口自动化测试')
@allure.story('自动化接口结果')
class TestBISHENGLogin:
    @pytest.fixture(scope="class")
    def global_session(self):
        """返回全局 Session 对象"""
        return SessionManager().get_session()

    def _get_public_key(self, session, endpoint):
        """获取RSA公钥"""
        res = session.get(f"{endpoint}/api/v1/user/public_key")
        res.raise_for_status()
        return res.json()["data"]["public_key"]

    def _encrypt_password(self, password, public_key):
        """RSA加密密码"""
        rsa_key = RSA.import_key(public_key)
        cipher = PKCS1_v1_5.new(rsa_key)
        encrypted = cipher.encrypt(password.encode())
        return base64.b64encode(encrypted).decode()

    @pytest.mark.parametrize("args", CONFDATA.login_cases())
    def test_login(self, args, global_session):
        case_id = args[0]['id']
        case_name = args[0]['case_name']

        with allure.step(f"测试用例 {case_id}: {case_name}"):
            # bisheng_ep = os.environ.get('TEST_BISHENG_EP')
            bisheng_ep = CONFDATA.config_dict['TEST_BISHENG_EP']

            # 1. 获取公钥
            with allure.step("获取RSA公钥"):
                public_key = self._get_public_key(global_session, bisheng_ep)
                allure.attach(f"公钥内容:\n{public_key}", "Public Key", allure.attachment_type.TEXT)

            # 2. 加密密码
            with allure.step("加密用户密码"):
                encrypted_pwd = self._encrypt_password("Dataelem@123", public_key)

            # 3. 执行登录
            with allure.step("提交登录请求"):
                login_data = {
                    "user_name": "sarah",
                    "password": encrypted_pwd
                }
                res = global_session.post(
                    f"{bisheng_ep}/api/v1/user/login",
                    json=login_data,
                    timeout=5
                )
                res.raise_for_status()

                # 将cookies附加到报告中
                cookies = global_session.cookies.get_dict()
                allure.attach(
                    str(cookies),
                    "获取到的Cookies",
                    allure.attachment_type.JSON
                )

                # 验证登录是否成功
                assert res.json().get("status_code") == 200, "登录失败"
                LogUtil().info(f"用例 {case_name} 执行成功")