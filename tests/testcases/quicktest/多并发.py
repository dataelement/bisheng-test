import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# 定义发送请求的函数
def send_request():
    url = "http://192.168.106.120:3002/api/v2/assistant/chat/completions"
    payload = json.dumps({
        "model": "07fc31f1-6f96-41d0-928c-8574bd1f6928",
        "messages": [
            {
                "role": "user",
                "content": "英语中的hello,翻译成中文"
            }
        ],
        "temperature": 0,
        "stream": True
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, headers=headers, data=payload)
    # 打印当前线程的名字和响应结果
    print(f"Thread {threading.current_thread().name}: {response.text}")
    return response.text

# 使用 ThreadPoolExecutor 并发执行多个请求
def send_requests_concurrently(num_requests=5):
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(send_request) for _ in range(num_requests)]
        results = []
        for future in as_completed(futures):
            results.append(future.result())
    return results

# 执行并获取结果
results = send_requests_concurrently(5)
for result in results:
    print(result)
