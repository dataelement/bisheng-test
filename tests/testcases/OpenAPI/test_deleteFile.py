import requests

url = "http://192.168.106.120:3002/api/v2/filelib/file/"

headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}

response = requests.request("DELETE", url, headers=headers)

print(response.text)