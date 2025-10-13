# -*- coding: utf-8 -*-
"""
@Time ： 2025/2/11 12:18
@Auth ： Sara
@File ：脑筋急转弯-流式.py
@IDE ：PyCharm
"""
import requests
import json

url = "http://192.168.106.120:3002/api/v2/workflow/invoke"

payload = json.dumps({
    "workflow_id": "0eed362e-d93d-4734-a112-4ea06c5960ac",
    "stream": "False",  # 启用流式传输
    # "input": {"input_2775b": {  # 事件里的节点ID
    #     # input_schme.value中元素的 key 以及对应要传入的值
    #     "user_input": "With the spirit of the forest guiding her, Lila led the charge to replant trees and clean up the debris"
    # }},
    "input": {},
    "message_id": "string",
    "session_id": "string"
})

headers = {
    'Content-Type': 'application/json'
}

# 使用POST方法发起工作流
response = requests.post(url, headers=headers, data=payload)
print(response.text)

# 检查响应是否正常
# if response.status_code == 200:
#     # 流式处理响应
#     for line in response.iter_lines():
#         if line:
#             # 解码并将每一行转换为字符串
#             message = line.decode('utf-8')
#             decoded_message = message.encode('utf-8').decode('unicode-escape')
#
#             print(decoded_message)  # 打印消息字符串
# else:
#     print(f"错误: {response.status_code} - {response.text}")
