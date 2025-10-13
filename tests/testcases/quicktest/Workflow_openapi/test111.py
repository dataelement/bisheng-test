# -*- coding: utf-8 -*-
"""
@Time ： 2025/7/2 11:57
@Auth ： Sara
@File ：test111.py
@IDE ：PyCharm
"""
import requests
import json
from sseclient import SSEClient

url = "http://192.168.106.120:3002/api/v2/workflow/invoke"

payload = json.dumps({
    "workflow_id": "f73d0e89d9dc42429dbdc439605000ff",
    "stream": False,
    # "input": {
    #     "input_55c94": {  # 事件里的节点ID
    #         # "output_result": "水"
    #         # "category": "脑筋急转弯"
    #
    #         #          # input_schme.value中元素的 key 以及对应要传入的值
    #                  "user_input": "今天贵州茅台股价情况"
    #
    #     }},
    # "message_id": "394645",
    # "session_id": "72f93b5d45d04782a16f047f8b167ce7_async_task_id"
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

# response1 = requests.request("POST", url, headers=headers, data=payload, stream=False)


print(response.text)
# print(response1.text)
