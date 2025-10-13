# -*- encoding: utf-8 -*-
'''
@File    :   test_upload.py
@Time    :   2024/05/29 16:41:32
@Author  :   Sara 
@Version :   1.0
'''
# flake8: noqa
import allure
import pytest
import requests

import os

@allure.epic('API服务接口自动化测试')
@allure.feature('执行环境')
@allure.story('upload接口自动化接口结果')
class UPLOAD:
    def uploadgfile(file_path):

        bisheng_ep = os.environ.get('TEST_BISHENG_EP')
        url = bisheng_ep + '/api/v1/knowledge/upload?file'
        headers = {}
        files = {'file': open(file_path, 'rb')}
        res = requests.post(url, headers=headers, files=files)
        file_path = res.json().get('data', {}).get('file_path', '')
        
        return file_path
