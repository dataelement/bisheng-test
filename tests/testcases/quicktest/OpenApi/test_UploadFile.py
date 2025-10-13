import requests

# API URL
url = "http://192.168.106.120:3002/api/v2/filelib/file/1572"

# 非文件 payload 参数
payload = {
    # 'callback_url': 'http://192.168.106.120:3002',
    'separator': ',',
    'chunk_size': '1024',
    'separator_rule': '["\\n\\n","\\n"]'
}

# 文件上传部分，文件的路径需要指定
# 假设你上传的文件名为 'example.txt'，路径为 '/path/to/your/file'
files = [
    ('file', ('合同.pdf', open('/Users/sara/Desktop/DataElem/dev/bisheng-test/data/test_data/合同.pdf', 'rb'), 'application/octet-stream'))
]

# 请求头信息，模拟 Apifox 的 User-Agent
headers = {
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}

# 发送 POST 请求
response = requests.post(url, headers=headers, data=payload, files=files)

# 打印响应结果
print(response.text)
