# -*- coding: utf-8 -*-
"""
@Time ： 2025/5/13 15:05
@Auth ： Sara
@File ：上传文件.py
@IDE ：PyCharm
"""
import requests


def upload_file():
    server = "http://192.168.106.120:3002"
    url = server + '/api/v1/knowledge/upload'
    headers = {}
    files = {'file': open('/Users/sara/Desktop/DataElem/dev/bisheng-test/data/test_data/合同.pdf', 'rb')}
    res = requests.post(url, headers=headers, files=files)
    print(res.content)
    file_path = res.json()['data'].get('file_path', '')
    # print(file_path + "111")
    return file_path


upload_file()
