# flake8: noqa
import base64
import os
import sys

import requests

server = "http://192.168.106.120:3002"


def api_call(user_name, password):
    # url = server + '/lab/ocr/predict/ticket'
    # url = server + '/lab/ocr/predict/table'
    # url = server + '/lab/ocr/predict/general'
    url = server + '/api/v1/user/regist'

    # b64 = base64.b64encode(open(image, 'rb').read()).decode()
    data = {'user_name': user_name, 'password': password}
    res = requests.post(url, json=data).json()
    return res
