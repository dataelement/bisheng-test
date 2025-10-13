
import requests
from typing import Optional

BASE_API_URL = "http://192.168.106.120:3002/api/v1/process"
FLOW_ID = "d4cfb643-c141-4f40-8b10-c69958e9db65"
# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "CombineDocsChain-GeeZU": {},
  "RetrievalQA-XLqYb": {},
  "Milvus-xi2X0": {},
  "ProxyChatLLM-13f55": {}
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
inputs = {"query":"中国的主席是","id":"RetrievalQA-XLqYb"}
print(run_flow(inputs, flow_id=FLOW_ID, tweaks=TWEAKS))