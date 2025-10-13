import requests

# 基础URL
url = "http://192.168.106.120:3002/api/v2/filelib/1573"

# 查询参数（用于DELETE请求）
payload = {
    # "knowledge_id": 1573
}

# 请求头
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}

# 使用DELETE请求，并通过params传递查询参数
response = requests.request("DELETE", url, headers=headers, data=payload)

# 打印响应内容
print(response.text)

