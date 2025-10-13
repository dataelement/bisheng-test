import requests
from typing import Optional

BASE_API_URL = "https://bisheng.dataelem.com/api/v1/process"
FLOW_ID = "05604714-d6aa-4ed3-b0c4-8658401af423"
# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
def upload_file(local_path: str):
    server = "https://bisheng.dataelem.com"
    url = server + '/api/v1/knowledge/upload'
    headers = {}
    files = {'file': open(local_path, 'rb')}
    res = requests.post(url, headers=headers, files=files)
    print(res.json())
    file_path = res.json()['data'].get('file_path', '')
    print(file_path)
    return file_path
file_path = upload_file("/Users/sara/Desktop/DataElem/dev/bisheng-test/data/test_data/合同.pdf")

TWEAKS = {
  "InputFileNode-53363": {"file_path": file_path},
  "PyPDFLoader-8afd7": {},
  "PromptTemplate-7bfb3": {},
  "StructuredOutputParser-350ea": {},
  "ResponseSchema-c52ad": {},
  "ResponseSchema-bd4d2": {},
  "ResponseSchema-b7c8b": {},
  "ResponseSchema-fc38e": {},
  "ResponseSchema-66a96": {},
  "ResponseSchema-c36dd": {},
  "ResponseSchema-83711": {},
  "ResponseSchema-d5fa2": {},
  "ResponseSchema-649f3": {},
  "HostQwenChat-0ca7d": {},
  "LLMChain-59d41": {}
}



def run_flow(inputs: dict, flow_id: str, file_path: str, tweaks: Optional[dict] = None) -> dict:
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
    payload["inputs"]["file_path"] = file_path  # Add the file_path to the inputs
    if "InputFileNode-53363" in tweaks:
        tweaks["InputFileNode-53363"]["file_path"] = file_path
    response = requests.post(api_url, json=payload)
    return response.json()


    # response = requests.post(api_url, json=payload)
    # return response.json()

# Setup any tweaks you want to apply to the flow
inputs = {"input":"","context":"","id":"LLMChain-59d41"}
print(run_flow(inputs, flow_id=FLOW_ID, file_path=file_path, tweaks=TWEAKS))