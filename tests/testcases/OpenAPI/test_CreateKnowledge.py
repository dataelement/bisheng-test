# -*- coding: utf-8 -*-
"""
@Time ： 2025/5/7 17:16
@Auth ： Sara
@File ：test_CreateKnowledge.py
@IDE ：PyCharm
"""
import requests
import json

url = "http://192.168.106.120:3002/api/v2/filelib/"

payload = json.dumps({
   "name": "api创建120版本",
   "description": "描述",
   "model": "161",
   "is_partition": True
})
headers = {
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)