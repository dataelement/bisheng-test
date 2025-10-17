# -*- coding: utf-8 -*-
"""
@Time ： 2025/5/8 10:39
@Auth ： Sara
@File ：test_DeleteFileBatch.py
@IDE ：PyCharm
"""
import requests
import json

url = "http://192.168.106.120:3002/api/v2/filelib/delete_file"

payload = json.dumps([
    38310,
    38309,
    38308,
    38307
])
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
