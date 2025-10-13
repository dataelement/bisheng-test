# -*- coding: utf-8 -*-
"""
@Time ： 2025/5/8 11:16
@Auth ： Sara
@File ：test_ClearTmpChunksData.py
@IDE ：PyCharm
"""
import requests
import json

url = "http://192.168.106.120:3002/api/v2/filelib/chunk_clear"

payload = json.dumps({
   "flow_id": "cd4bdfb0080c4f288f562dab46f480c4",
   "chat_id": "b2a07bf2a7c52cb60f6e3667d8b299a7"
})
headers = {
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)