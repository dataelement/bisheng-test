import base64
import os
import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

class CookieManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CookieManager, cls).__new__(cls)
            cls._instance.cookies = {}
            cls._instance.session = requests.Session()
            cls._instance.base_url = os.environ.get('API_BASE_URL', 'http://192.168.106.120:3002')
        return cls._instance

    def _get_public_key(self):
        """获取RSA公钥"""
        url = f"{self.base_url}/api/v1/user/public_key"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()["data"]["public_key"]

    def _encrypt_password(self, password, public_key):
        """RSA加密密码"""
        rsa_key = RSA.import_key(public_key)
        cipher = PKCS1_v1_5.new(rsa_key)
        encrypted = cipher.encrypt(password.encode())
        return base64.b64encode(encrypted).decode()

    def get_cookies(self, user_name=None, password=None):
        """
        获取cookies（如果未登录则自动登录）
        参数:
            user_name (str): 用户名（可选，如果不传则尝试从环境变量读取）
            password (str): 密码（可选，如果不传则尝试从环境变量读取）
        返回:
            dict: cookies字典（如果登录失败则返回None）
        抛出:
            ValueError: 如果未提供登录凭据且无缓存cookies
        """
        if not self.cookies:
            # 如果未提供用户名密码，尝试从环境变量获取
            if not (user_name and password):
                user_name = os.environ.get("API_USERNAME")
                password = os.environ.get("API_PASSWORD")
                if not (user_name and password):
                    raise ValueError("未提供登录凭据且无缓存cookies")

            # 执行登录
            try:
                public_key = self._get_public_key()
                encrypted_pwd = self._encrypt_password(password, public_key)

                url = f"{self.base_url}/api/v1/user/login"
                payload = {
                    'user_name': user_name,
                    'password': encrypted_pwd
                }
                headers = {
                    'Content-Type': 'application/json'
                }

                response = self.session.post(url, json=payload, headers=headers)
                response.raise_for_status()

                if response.json().get('status_code') == 200:
                    self.cookies = self.session.cookies.get_dict()
                else:
                    return None  # 登录失败
            except Exception as e:
                print(f"登录失败: {str(e)}")
                return None

        return self.cookies