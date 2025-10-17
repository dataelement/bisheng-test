# import requests

# # 基础URL不包含查询参数
# url = "http://192.168.106.120:3002/api/v2/filelib/"

# # 查询参数
# params = {
#     "name": "1111222"
# }

# headers = {
#    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
# }

# # 发出带有查询参数的GET请求
# response = requests.get(url, headers=headers, params=params)

# # 打印响应文本
# print(response.text)
import requests
# 读取所有知识库信息.

url = "http://192.168.106.120:3002/api/v2/filelib/"

payload={
    # "name":"1111222"
     "page_size":20,
     "page_num":2

}
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}

response = requests.request("GET", url, headers=headers, params=payload)

print(response.text)