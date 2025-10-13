
import requests
from typing import Optional

BASE_API_URL = "http://192.168.106.120:3002/api/v1/process"
FLOW_ID = "2377ee17-3595-4157-a7f1-713a89f978bc"
# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "CombineDocsChain-Pud2p": {},
  "RetrievalQA-qH6Mk": {},
  "OpenAIProxyEmbedding-yvld7": {},
  "InputFileNode-jdLkB": {"file_path":"http://192.168.106.116:9000/tmp-dir/%E5%BC%80%E5%8F%91%E5%AE%9E%E8%B7%B5.docx?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin%2F20240829%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240829T112056Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=7d45cef897af832ec784d2370ec0c40779e3ffd8ec94e242eb9c362bce9ca5a0"},
  "ProxyChatLLM-rnE4s": {},
  "Milvus-T3kRH": {},
  "ElemUnstructuredLoaderV0-LAGXM": {},
  "RecursiveCharacterTextSplitter-a7fc9": {}
}

def run_flow(inputs: dict, flow_id: str, tweaks: Optional[dict] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param flow_id: The ID of the flow to run
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/{flow_id}"

    payload = {"inputs": inputs}

    if tweaks:
        payload["tweaks"] = tweaks

    response = requests.post(api_url, json=payload)
    return response.json()

# Setup any tweaks you want to apply to the flow
inputs = {"query":"你好","id":"RetrievalQA-qH6Mk"}
print(run_flow(inputs, flow_id=FLOW_ID, tweaks=TWEAKS))