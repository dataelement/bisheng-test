# -*- coding: utf-8 -*-
"""
@Time ： 2025/5/14 16:09
@Auth ： Sara
@File ：test_DeleteQA.py
@IDE ：PyCharm
"""
import requests

url = "http://192.168.106.120:3002/api/v2/filelib/qa/1464"

payload={}
headers = {}

response = requests.request("DELETE", url, headers=headers, data=payload)

print(response.text)