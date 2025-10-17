# -*- coding: utf-8 -*-
"""
@Time ： 2025/5/14 16:14
@Auth ： Sara
@File ：test_GetQADetail.py
@IDE ：PyCharm
"""
import requests

url = "http://192.168.106.120:3002/api/v2/filelib/detail_qa?id=1462"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)