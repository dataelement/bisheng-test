import requests

url = "http://192.168.106.120:3002/api/v2/filelib/file/list?knowledge_id=1570&page_num=1&page_size=1&status=2"

headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}

response = requests.request("GET", url, headers=headers)

print(response.text)