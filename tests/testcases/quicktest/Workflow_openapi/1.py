
# -*- coding: utf-8 -*-
"""
@Time ： 2025/2/11 15:34
@Auth ： Sara
@File ：读取文件作为user_input.py
@IDE ：PyCharm
"""

import requests
import json

# 第一步：直接从 test.txt 文件中读取文本
with open('/Users/sara/Desktop/DataElem/dev/bisheng-test/tests/testcases/quicktest/Workflow_openapi/test.txt', 'r', encoding='utf-8') as file:
    user_input = file.read()

# 第二步：定义 API 的 URL 和请求负载
url = "http://192.168.106.120:3002/api/v2/workflow/invoke"

payload = json.dumps({
    "workflow_id": "99e50566-f194-4cf5-b5cb-22b9758e04fd",
    "stream": True,  # 启用流式传输
    "input": {
        "input_5212f": {
            "text_input": user_input,  # 使用从文件中读取的文本
            "category": "检查错误"
        }},
    "message_id": "384938",
    "session_id": "b9c20ee95d874ef88704f88e34b97b79_async_task_id"
})

headers = {
    'Content-Type': 'application/json'
}

# 第三步：使用 POST 方法发起工作流
response = requests.post(url, headers=headers, data=payload)

# 第四步：处理流式输出
# output_result = ""

def process_stream(response):
    output_result = ""

    for message in response.json().get('data', {}).get('data', []):
        if message['event'] == 'stream_msg':
            output_result += message['output_schema'].get('message', '')
        elif message['event'] == 'close':
            print("完整的输出是:", output_result)
            break

# 调用处理流的函数
process_stream(response)

# 如果需要直接打印响应，可以这样
print(response.text)