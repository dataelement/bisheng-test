# -*- coding: utf-8 -*-
# @Time    : 2025/9/4 20:59
# @Author  : sara
# @Email   : your-email@example.com
# @File    : workflow.py

import requests
import json

url = "http://192.168.106.120:3002/api/v2/workflow/invoke"

payload = json.dumps({
   "workflow_id": "98bf493b94694dfd955940cf822f6c70",
   "stream": False, # 为空或者不传，都会请求流式返回工作流事件。本示例为了直观展示返回结果，所以改
    "input": {"input_914b0": {  # 事件里的节点ID
        "user_input": "贵州茅台股价情况"  # 使用从文件中读取的文本
    }},
    "message_id": "403664",
    "session_id": "f94f002c37c741f489aab53dd836a646_async_task_id"
})

headers = {
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)# 输出工作流的响应