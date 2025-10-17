# -*- coding: utf-8 -*-
"""
@Time ： 2025/5/14 16:06
@Auth ： Sara
@File ：test_AddRelactive_qa.py
@IDE ：PyCharm
"""
import requests
import json

url = "http://192.168.106.120:3002/api/v2/filelib/add_relative_qa"

payload = json.dumps({
   "knowledge_id": 1587,
   "data": {
      "relative_questions": ["1111"],
      "id": "1462"
   },
   "user_id": 0
})
headers = {
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)