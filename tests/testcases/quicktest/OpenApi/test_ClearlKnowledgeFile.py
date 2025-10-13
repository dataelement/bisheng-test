# 清空知识库中的文件
import requests

url = "http://192.168.106.120:3002/api/v2/filelib/clear/1572"

headers = {
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}

response = requests.request("DELETE", url, headers=headers)

print(response.text)
