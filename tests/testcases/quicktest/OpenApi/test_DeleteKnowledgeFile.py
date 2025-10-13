# -*- coding: utf-8 -*-
"""
@Time ： 2025/5/7 19:35
@Auth ： Sara
@File ：test_DeleteKnowledgeFile.py
@IDE ：PyCharm
"""
import requests

url = "http://192.168.106.120:3002/api/v2/filelib/file/38121"

payload={}
headers = {}

response = requests.request("DELETE", url, headers=headers, data=payload)

print(response.text)