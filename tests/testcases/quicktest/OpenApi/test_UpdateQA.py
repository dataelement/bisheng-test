# -*- coding: utf-8 -*-
"""
@Time ： 2025/5/14 16:12
@Auth ： Sara
@File ：test_UpdateQA.py
@IDE ：PyCharm
"""
import requests
import json

url = "http://192.168.106.120:3002/api/v2/filelib/update_qa"

payload = json.dumps({
   "id": 1462,
   "question": "hhhh",
   "answer": [
      "string"
   ]
})
headers = {
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)