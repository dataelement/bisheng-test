from datetime import time, datetime
import requests
import os
import json
import base64
from tests.testcases import bisheng_api

from tests.utils.image_util import convert_b64


class HttpUtils:
    @staticmethod
    def http_post_login(headers, url, parameters):
        if isinstance(parameters, dict):
            res = requests.post(url, json=parameters, headers=headers)
        else:
            res = requests.post(url, data=parameters, headers=headers)
        if res.status_code not in [200, 201]:
            raise Exception(u"请求异常")
        result = json.loads(res.text)
        return result

    @staticmethod
    def http_post(headers, url, parameters):
        if isinstance(parameters, dict):
            res = requests.post(url, json=parameters, headers=headers)
        else:
            res = requests.post(url, data=parameters, headers=headers)
        if res.status_code != 200:
            raise Exception(u"请求异常")
        result = json.loads(res.text)
        return result

    @staticmethod
    def http_get(headers, url):
        req_headers = json.dumps(headers)
        # print("接口请求url：" + url)
        # print("接口请求headers：" + req_headers)
        res = requests.get(url, headers=headers)
        # print("接口返回结果：" + res.text)
        if res.status_code != 200:
            raise Exception(u"请求异常")
        result = json.loads(res.text)
        return result


def prepare_data_regist(args, TEST_HOST):
    headers = {"Content-Type": "application/json"}
    url = TEST_HOST + args['url']
    # 格式化日期为'YYYY-MM-DD'
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    args['body']['user_name'] = current_date
    res = HttpUtils.http_post_login(headers, url, args['body'])
    return res


def prepare_data_login(args, bisheng_ep):
    headers = {"Content-Type": "application/json"}
    url = bisheng_ep + args[0]['url']
    res = HttpUtils.http_post_login(headers, url, args[0]['body'])
    return res


def prepare_data(args, TEST_HOST):
    headers = {"Content-Type": "application/json"}
    # url = "http://" + TEST_HOST + ":" + TEST_PORT + args['url']
    url = TEST_HOST + args['url']
    res = HttpUtils.http_post(headers, url, args['body'])
    # res = HttpUtils.http_post(headers, url, args['body'])
    return res


def prepare_data_knowlagecreate(args, TEST_HOST):
    access_token="""
      eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJ1c2VyX25hbWVcIjogX
      CJhZG1pblwiLCBcInVzZXJfaWRcIjogMSwgXCJyb2xlXCI6IFwiYWRtaW5cIn0iLCJpYXQ
      iOjE2OTk5MzM4MTUsIm5iZiI6MTY5OTkzMzgxNSwianRpIjoiOGFhNzY4M2MtM2MyMS00Y
      zRlLTk4OGEtNzgwYmFhNzNiODFkIiwiZXhwIjoxNzAwMDIwMjE1LCJ0eXBlIjoiYWNjZXN
      zIiwiZnJlc2giOmZhbHNlfQ.uNm-DRq5BCBSg_1S0aRMn-sS02r1UEMf8wedrb1Tzy4; r
      efresh_token_cookie=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZ
      G1pbiIsImlhdCI6MTY5OTkzMzgxNSwibmJmIjoxNjk5OTMzODE1LCJqdGkiOiI1OTVjZjc
      2MS05NGM4LTRiZjItOWViNC1iYzFmOWZmYjVjYTgiLCJleHAiOjE3MDI1MjU4MTUsInR5c
      GUiOiJyZWZyZXNoIn0.r-ZqYQIZtt4V4wEQjsYnzq8uf5LH6Z6gd8yz4MyQhvQ
    """

    _norm_str = lambda s: s.replace('\n', '').replace(' ', '')

    headers = {
      "Content-Type": "application/json",
      'Cookie': 'access_token_cookie=%s' % _norm_str(access_token)
    }
    url =  TEST_HOST + args['url']
     # 格式化日期为'YYYY-MM-DD'
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    args['body']['name'] = current_date
    res = HttpUtils.http_post_login(headers, url, args['body'])
    # res = HttpUtils.http_post(headers, url, args['body'])
    return res


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
