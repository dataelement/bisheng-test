import requests
import json
import time

# API端点
url = "http://192.168.106.120:3002/api/v2/assistant/chat/completions"

# 请求数据
payload = json.dumps({
    "model": "b19ed2c180e94775815d8750794fe05c",
    "messages": [
        {
            "role": "user",
            "content": "如何根据我的财务状况和风险偏好制定投资计划"
        }
    ],
    "temperature": 0,
    "stream": True  # 启用流式输出
})

# 请求头
headers = {
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Content-Type': 'application/json',
    'Accept': 'text/event-stream'  # 明确要求流式响应
}


def process_stream_response(response):
    """
    处理流式响应
    """
    try:
        # 检查响应状态
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            print(response.text)
            return

        print("开始接收流式数据...\n")

        # 逐行处理流式数据
        buffer = ""  # 用于累积不完整的数据
        for line in response.iter_lines():
            if line:  # 过滤空行
                try:
                    decoded_line = line.decode('utf-8')

                    # 调试用：打印原始数据
                    # print(f"原始数据: {decoded_line}")

                    # 处理可能的两种流式格式：
                    # 1. SSE格式: data: {...}
                    # 2. 纯JSON格式: {...}
                    if decoded_line.startswith('data:'):
                        data_str = decoded_line[5:].strip()
                    else:
                        data_str = decoded_line.strip()

                    # 跳过结束标记
                    if data_str == "[DONE]":
                        continue

                    # 尝试解析JSON
                    try:
                        data = json.loads(data_str)
                    except json.JSONDecodeError:
                        # 可能是数据不完整，先缓存
                        buffer += data_str
                        try:
                            data = json.loads(buffer)
                            buffer = ""  # 清空缓存
                        except json.JSONDecodeError:
                            continue  # 继续等待更多数据

                    # 提取并打印内容
                    if 'choices' in data and data['choices']:
                        choice = data['choices'][0]
                        if 'delta' in choice and 'content' in choice['delta']:
                            content = choice['delta']['content']
                            print(content, end='', flush=True)  # 实时输出
                            time.sleep(0.02)  # 稍微延迟，模拟流式效果

                    # 检查是否结束
                    if 'finish_reason' in choice and choice['finish_reason']:
                        print("\n\n流式传输完成")
                        break

                except Exception as line_error:
                    print(f"\n处理数据行时出错: {line_error}")
                    continue

    except Exception as e:
        print(f"\n处理流式响应时出错: {e}")


def main():
    try:
        # 发送请求（启用流式）
        response = requests.post(
            url,
            headers=headers,
            data=payload,
            stream=True,
            timeout=30  # 设置超时
        )

        # 处理响应
        process_stream_response(response)

    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")
    finally:
        print("\n程序结束")


if __name__ == "__main__":
    main()