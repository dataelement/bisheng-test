# -*- coding: utf-8 -*-
"""
@Time ： 2025/5/14 15:55
@Auth ： Sara
@File ：test_AddQA.py
@IDE ：PyCharm
"""
import requests
import json

url = "http://192.168.106.120:3002/api/v2/filelib/add_qa"

payload = json.dumps({
   "knowledge_id": 1587,
   "data": [
      {
         "question": "API添加QA知识库``",
         "answer": [
            "添加成功了"
         ]
      }
   ],
   "user_id": 12
})
headers = {
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)