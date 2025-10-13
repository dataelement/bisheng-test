import requests
import json

url = "http://192.168.106.120:3002/api/v2/filelib/chunks_string"

payload = json.dumps({
   "knowledge_id": 1572,
   "documents": [
      {
         "page_content": "小猫一般活多久？",
         "metadata": {
            "source": "宠物百科.txt",
            "answer": "小猫一般活N年",
            "url": "www.baidu.com?keyword=小猫活多久"
         }
      },
      {
         "page_content": "小猫爱吃什么？",
         "metadata": {
            "source": "宠物百科.txt",
            "answer": "小猫爱吃鱼",
            "url": "www.baidu.com?keyword=小猫爱吃什么"
         }
      }
   ]
})
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)