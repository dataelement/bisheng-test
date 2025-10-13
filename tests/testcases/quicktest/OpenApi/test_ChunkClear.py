import requests
import json

url = "http://192.168.106.120:3002/api/v2/filelib/chunk_clear"

payload = json.dumps({
#    "flow_id": "d4cfb643-c141-4f40-8b10-c69958e9db65",
#    "chat_id": "98c6b4f961e3f22cf10dc5f161111f05"
})
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)