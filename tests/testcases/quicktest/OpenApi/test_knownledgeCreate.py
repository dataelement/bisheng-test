import requests
import json

url = "http://192.168.106.120:3002/api/v2/filelib/"

payload = json.dumps({
   "name": "V2接口创建",
   "description": "",
   "model": "10"
   # "is_partition": True
})
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)