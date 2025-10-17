# -*- coding: utf-8 -*-
"""
@Time ： 2025/5/14 16:15
@Auth ： Sara
@File ：test_QAList.py
@IDE ：PyCharm
"""
import requests
import json

url = "http://192.168.106.120:3002/api/v2/filelib/query_qa"

payload = json.dumps({
   "timeRange": [
      "2025-05-11",
      "2025-05-15"
   ]
})
headers = {
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)