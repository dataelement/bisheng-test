import requests

url = "http://192.168.106.120:3002/api/v2/filelib/chunks"

payload={
    "knowledge_id":"1572",
    "metadata": {
        # "source": "宠物百科.txt",
        "answer": "小猫一般活N年",
        "url": "www.baidu.com?keyword=小猫活多久"
    },
    "separator_rule":["\\n\\n","\\n"],
    "chunk_size":"1000",
    "chunk_overlap":"100"
}
files=[
   ('file',('合同.pdf',open('/Users/sara/Desktop/DataElem/dev/bisheng-test/data/test_data/合同.pdf','rb'),'application/octet-stream'))
]
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)