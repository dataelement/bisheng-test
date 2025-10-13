# -*- coding: utf-8 -*-
"""
@Time ： 2025/2/11 15:34
@Auth ： Sara
@File ：读取文件作为user_input.py
@IDE ：PyCharm
"""
import requests
import json

# 第一步：直接从1.txt文件中读取文本
# with open('/Users/sara/Desktop/DataElem/dev/bisheng-test/tests/testcases/quicktest/Workflow_openapi/test.txt', 'r',
#           encoding='utf-8') as file:
#     user_input = file.read()
# print("从1.txt中读取的文本:")
# print(user_input)

# 第二步：定义API的URL和请求负载
url = "http://192.168.106.120:3002/api/v2/workflow/invoke"

payload = json.dumps({
    "workflow_id": "1be8ec1f62924504a1de7479ef7b0d5c",
    "stream": False,  # 启用流式传输

    # # QA知识库
    "input": {
        "input_8dc96": {  # 事件里的节点ID
            # key是input_schme.value中元素的 key 以及对应要传入的值
            # "text_input": "你是谁",
            "user_input": "合同签约日期",
            # "file": ["http://192.168.106.116:9000/tmp-dir/%E5%90%88%E5%90%8C.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin%2F20250513%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250513T075038Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=44f531aa9938b5449dfb0c236b440a81e7c5a1374d544385cca82dfdf9124f9d"]
            # 用户上传文件获取到的文件url, 允许多选就是多个url
            # "category": "1,2"  # 将选项内容赋值给变量。当允许多选时，多个选项内容通过逗号分隔。
            "dialog_files_content": ["http://192.168.106.116:9000/tmp-dir/%E5%90%88%E5%90%8C.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin%2F20250515%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250515T071156Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=fac04713760a3ce1f0408326074a86fc51697fa9415e2a5b98f1d49aa3bc74c8"]
            #
        }},
    "message_id": "397516",
    "session_id": "23caa1f827b64b57bc33ac2b1d804269_async_task_id"
})

# 脑筋急转弯
# "input": {
#     "output_d65e8": {  # 事件里的节点ID
#         # "category": "脑筋急转弯"  # 将选项内容赋值给变量。当允许多选时，多个选项内容通过逗号分隔。
#         "output_result": "我不知道"
#     }},
# 选择脑筋急转弯
# "input": {
#     "input_eb2b4": {  # 事件里的节点ID
#         "category": "脑筋急转弯"  # 将选项内容赋值给变量。当允许多选时，多个选项内容通过逗号分隔。
#     }},
# 第三步： 选择试试
# "input": {
#     "output_71010": {  # 事件里的节点ID
#         "output_result": "4e04164f"
#     }},
# "input": {
#     "output_a5bee": {  # 事件里的节点ID
#         # "category": "脑筋急转弯"  # 将选项内容赋值给变量。当允许多选时，多个选项内容通过逗号分隔。
#         "output_result": "99b4de59"
#     }},
# "message_id": "385108",
# "session_id": "7dff07aff17c4c9eb40385253593e836_async_task_id"
# })
# dialog_input
# "input": {
#     "input_5212f": {  # 事件里的节点ID
#     "user_input": "25  睡不着失眠多梦"  # 使用从文件中读取的文本
# }},
headers = {
    'Content-Type': 'application/json'
}

# 第三步：使用POST方法发起工作流
response = requests.post(url, headers=headers, data=payload)
print(response.text)
