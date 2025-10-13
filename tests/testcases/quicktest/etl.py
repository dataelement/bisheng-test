# -*- coding: utf-8 -*-
# @Time    : 2025/8/22 14:35
# @Author  : sara
# @Email   : your-email@example.com
# @File    : etl.py
import base64
import os
import requests

url = "http://192.168.106.12:8012/v1/etl4llm/predict"
#filename = "./我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他的我的我的我的你的他.pdf"
filename = "/Users/sara/Desktop/DataElem/dev/bisheng-test/tests/testcases/quicktest/API std 610 TWELFTH EDITION, SEPTEMBER 2021 Centrifugal Pumps for Petroleum,Petrochemical and Natural Gas industries.pdf"
b64_data = base64.b64encode(open(filename, "rb").read()).decode()
inp = dict(
    filename=os.path.basename(filename),
    b64_data=[b64_data],
    force_ocr=True,
    enable_formula=False,

    #ocr_sdk_url="",
    ocr_sdk_url="http://192.168.106.12:8502"

    )
resp = requests.post(url, json=inp).json()
print(resp)