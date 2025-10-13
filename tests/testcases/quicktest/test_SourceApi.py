
# 第一步执行api访问
import requests


def _test_python_api():
    url = "http://192.168.106.120:3002/api/v1/process/e274b0fc-2640-44ef-9ee6-e1345f6ec421"
    body_json = {
        "inputs": {
            "question": "你好，总结下知识库内容",
            "id": "ConversationalRetrievalChain-SmY3w"
        },
        "tweaks": {
            "MixEsVectorRetriever-J35CZ": {},
            "Milvus-cyR5W": {},
            "ElasticKeywordsSearch-31Et9": {},
            "ConversationalRetrievalChain-SmY3w": {},
            "ConversationBufferMemory-K1tss": {},
            "PromptTemplate-bs0vj": {},
            "BishengLLM-f46ea": {}
        }
    }
    resp = requests.post(url, json=body_json)
    # 返回实例
    # result 对象中，source != 0 表示可以溯源
    # 通过 message_id查询溯源的数据
    # {
    #     "result": {
    #         "answer":
    #         "SQLAgent 是 Microsoft SQL Server 中的一个组件，它是一个作业调度程序，用于自动执行和管理 SQL Server 数据库中的作业和任务。SQLAgent 可以通过计划和配置来执行诸如备份、恢复、数据清理和索引重建等操作。它还可以设置警报和通知，以便管理员能够及时了解数据库中的问题和事件。",
    #         "source": 1,
    #         "message_id": 30522
    #     },
    #     "session_id": "A61GFF:538546578b93520116fe329d8df03e9805354919b50c8a946a0b47fa565ee350",
    #     "backend": "anyio"
    # }
    # 0: 不溯源
    # 1: 普通溯源
    # 2: 有访问权限限制溯源
    # 3: 知识库外部链接溯源
    # 4: QA溯源

# 第二步，获取溯源内容
def get_source(message_id):
    # keywords  是表示当前答案，有哪些关键字, 非必要
    keywords_url = f"http://192.168.106.120:3002/api/v1/qa/keyword?message_id={message_id}"
    keyword_resp = requests.get(keywords_url)

    # chunk 获取接口，当我们需要根据关键字进行排序，需要将上一个关键字的结果，拼接到keys 参数下。 ";" 分割
    chunk_url = f"http://192.168.106.120:3002/api/v1/qa/chunk?message_id={message_id}&keys="
    chunks = requests.get(chunk_url)
    print(chunks)
    #
    # {
#     "data": [{
#         "chunk_bboxes": [{
#             "page": 1,
#             "bbox": [90, 74, 226, 85]
#         }],  # 用来定位文本位置
#         "right": true,
#         # 双层pdf 路径
#         "source_url":
#         "http://110.16.193.170:50061/bisheng/10832?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T060923Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=053b4f399bbf3bdf3f4c86f750419bfde3739b4a2eee3e5490c4b63030ce66e5",
#         # 原始文件路径
#         "original_url":
#         "http://110.16.193.170:50061/bisheng/original/10832?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T060923Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=5ad4e49c5ff47aff425f472dbe21b11ce6d3ab65964292f61d1412a0ec07a3a6",
#         "score": 0,
#         "file_id": 10832,
#         "source": "多少专利和知识产权.pdf"
#     }],
#     "msg":
#     "success"
# }