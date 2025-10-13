import requests
import json

url = "http://192.168.106.120:3002/api/v2/assistant/chat/completions"

payload = json.dumps({
   "model": "a471efc9-34b2-4de7-9db7-1df6c30af035",
   "messages": [
      {
         "role": "user",
         "content": "你好"
      }
   ],
   "temperature": 0,
   "stream": True
})
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)