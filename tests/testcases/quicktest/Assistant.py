
from openai import OpenAI
base_url = "http://192.168.106.120:3002/api/v2/assistant"
model = "75c0343bcea4438e8b154c16c5c6e6cf"
client = OpenAI(base_url=base_url, api_key="empty")
# Round 1
messages = [{"role": "user", "content": "如何根据我的收入和支出制定个性化的理财计划?"}]
response = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True
)
reasoning_content = ""
content = ""
for chunk in response:
    if chunk.choices[0].delta.model_extra.get("reasoning_content"):
        if not reasoning_content:
            print("\n\n-----Reasoning Content-----\n")
        reasoning_chunk = chunk.choices[0].delta.reasoning_content
        print(reasoning_chunk, end='', flush=True)  # 流式打印reasoning
        reasoning_content += reasoning_chunk
    elif chunk.choices[0].delta.content:
        if not content:
            print("\n\n-----Final content-----\n")
        content_chunk = chunk.choices[0].delta.content
        print(content_chunk, end='', flush=True)  # 流式打印答案
        content += content_chunk