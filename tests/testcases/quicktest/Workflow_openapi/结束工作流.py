# -*- coding: utf-8 -*-
"""
@Time ： 2025/2/13 16:25
@Auth ： Sara
@File ：结束工作流.py
@IDE ：PyCharm
"""
import requests
import json

url = "http://192.168.106.120:3002/api/v2/workflow/stop"

payload = json.dumps({
   "workflow_id": "b595cf2dd8f34efaa30f02a0eacd8490",
   "session_id": "72f93b5d45d04782a16f047f8b167ce7_async_task_id"
})
headers = {
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)