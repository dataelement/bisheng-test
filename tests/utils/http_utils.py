from datetime import time, datetime
import requests
import os
import json
import base64
from tests.testcases.cookie_manager import CookieManager
from tests.testcases import bisheng_api, get_cookies
from tests.utils.image_util import convert_b64


class HttpUtils:
    # cookie_manager = CookieManager()
    # cookies = CookieManager().get_cookies(user_name="sarah", password="Dataelem@123")

    @staticmethod
    def http_post(headers, url, parameters):
        # cookies = CookieManager.get_cookies # 假设 CookieManager 有 get_cookies() 方法
        cookies = get_cookies()


        if isinstance(parameters, dict):
            res = requests.post(url, json=parameters, headers=headers, cookies=cookies)
            print("👏接口请求url：" + url)
            print("👏接口返回结果：" + res.text)
        else:
            res = requests.post(url, data=parameters, headers=headers,cookies=cookies)

        result = json.loads(res.text)
        print(result)

        if result['status_code'] != 200:
            # raise Exception("Request failed with status code: {}".format(result['status_code']))
            raise RuntimeError(f"Request failed with status code: {result['status_code']}")
        return result
    
    @staticmethod
    def http_delete(headers, url, parameters):
        if isinstance(parameters, dict):
            res = requests.delete(url, json=parameters, headers=headers)
        else:
            res = requests.delete(url, data=parameters, headers=headers)
        # if res.status_code not in [200, 201]:
        #     print(res.status_code)
        #     raise Exception(u"请求异常")
        result = json.loads(res.text)
        return result

    @staticmethod
    def http_get(headers, url):
        req_headers = json.dumps(headers)
        # print("接口请求url：" + url)
        # print("接口请求headers：" + req_headers)
        res = requests.get(url, headers=headers)
        # print("接口返回结果：" + res.text)
        # if res.status_code != 200:
        #     raise Exception(u"请求异常")
        result = json.loads(res.text)
        return result


def prepare_data_regist(args, bisheng_ep):
    headers = {"Content-Type": "application/json"}
    url = bisheng_ep + args[0]['url']
    # 格式化日期为'YYYY-MM-DD'
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    args[0]['body']['user_name'] = current_date
    res = HttpUtils.http_post(headers, url, args[0]['body'])
    return res

# sara
def prepare_data(args, bisheng_ep):
    # cookie_manager = CookieManager()
    # cookies = get_cookies()
    headers = {
      "Content-Type": "application/json",
      # 'Cookie': cookies
    }

    url = bisheng_ep + args[0]['url']
    res = HttpUtils.http_post(headers, url, args[0]['body'])
    return res

def prepare_dataqa(args, bisheng_ep, flowid):
    # file_path = os.path.join('COOKIE_PATH','/Users/sara/Desktop/DataElem/dev/bisheng-test/data/Cookie.txt')
    # with open(file_path, 'r') as file:  
    #     cookie_data = file.read() 
    headers = {
      "Content-Type": "application/json",
    #   'Cookie': cookie_data
    }
    url = bisheng_ep + args[0]['url'] + flowid
    res = HttpUtils.http_post(headers, url, args[0]['body'])
    return res

def prepare_data_get(args, bisheng_ep):
    file_path = os.path.join('COOKIE_PATH','/Users/sara/Desktop/DataElem/dev/bisheng-test/data/Cookie.txt')
    with open(file_path, 'r') as file:  
        cookie_data = file.read() 
    headers = {
      "Content-Type": "application/json",
      'Cookie': cookie_data
    }
    url = bisheng_ep + args[0]['url']
    res = HttpUtils.http_get(headers, url)
    return res

#单文档问答
def single_document(args, bisheng_ep, flowid, file_path):
    headers = {
      "Content-Type": "application/json",
    #   'Cookie': cookie_data
    }
    
    args[0]['tweaks']['InputFileNode-050e5']['file_path'] = file_path
    # args[0]['body'] = args[0]['body'] + args[0]['tweaks']
    args[0]['body']['tweaks'] = args[0]['tweaks']

    url = bisheng_ep + args[0]['url'] + flowid
    res = HttpUtils.http_post(headers, url, args[0]['body'])
    return res

# 上传文档接口
def uploadgfile(file_path):

        bisheng_ep = os.environ.get('TEST_BISHENG_EP')
        url = bisheng_ep + '/api/v1/knowledge/upload?file'
        headers = {}
        files = {'file': open(file_path, 'rb')}
        res = requests.post(url, headers=headers, files=files)
        file_path = res.json().get('data', {}).get('file_path', '')
        
        return file_path

# def prepare_data_knowledgecreate(args, bisheng_ep):
#     file_path = os.path.join('COOKIE_PATH','/Users/sara/Desktop/DataElem/dev/bisheng-test/data/Cookie.txt')
#     with open(file_path, 'r') as file:  
#         cookie_data = file.read() 
#     headers = {
#       "Content-Type": "application/json",
#       'Cookie': cookie_data
#     }
#     url = bisheng_ep + args[0]['url'] 
#      # 格式化日期为'YYYY-MM-DD'
#     current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     args[0]['body']['name'] = args[0]['body']['name'] + current_date 
#     res = HttpUtils.http_post(headers, url, args[0]['body'])
#     return res


def unstructuredLoaderv0(args, TEST_HOST_UNSTRUCTURED):
    url = "http://" + TEST_HOST_UNSTRUCTURED + args['url']
    # 直接获取图片路径，后续图片单独放机器上
    data_path = os.environ.get('DATA_PATH', '/app/data')
    filename = os.path.join(data_path, "demoImgaes", args['body']['filename'])
    # 根据图片地址获取图片信息
    args['body']['filename'] = convert_b64(filename)  
    b64_data = base64.b64encode(open(filename, "rb").read()).decode()
    inp = dict(
        filename=os.path.basename(filename),
        b64_data=[b64_data],
        mode="text")
    res = requests.post(url, json=inp).json()
    return res


def prepare_data_delete(args, bisheng_ep):
    file_path = os.path.join('COOKIE_PATH','/Users/sara/Desktop/DataElem/dev/bisheng-test/data/Cookie.txt')
    with open(file_path, 'r') as file:  
        cookie_data = file.read() 
    headers = {
      "Content-Type": "application/json",
      'Cookie': cookie_data
    }
    url = bisheng_ep + args[0]['url'] +str(args[0]['body']['id'])
    print(args[0]['body']['id'])

    res = HttpUtils.http_delete(headers, url, args[0]['body'])
    return res