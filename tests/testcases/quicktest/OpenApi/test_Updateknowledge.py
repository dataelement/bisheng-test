import requests
import json

url = "http://192.168.106.120:3002/api/v2/filelib/"

payload = json.dumps({
   "name": "",
   "description": "",
   "knowledge_id": 1570
})
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)