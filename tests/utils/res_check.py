# flake8: noqa
import allure
import os
import json
import sys

import Levenshtein


def check_normal_res(status_report, api_res, expectdata):
    if str(api_res) != str(expectdata):
        print("\tDIFF: 返回信息对比结果 不一致")
        print("\t期望结果: {}".format(str(expectdata)))
        print("\t请求结果: {}".format(str(api_res)))
        status_report += "DIFF: message 不一致\n" + \
                         "期望结果: {}\n".format(str(expectdata)) + \
                         "请求结果: {}\n".format(str(api_res))
    else:
        status_report += "SUCC: 所有信息 一致\n"
        print("SUCC: 所有信息 一致\n")
        return status_report


def check_normal_knowlageres(status_report, api_res, expectdata):
    if str(api_res['result']['result']) != str(expectdata['result']['result']):

        # 比较api_res里边result的diff，如果编辑距离<10，则认为相等
        diff = Levenshtein.distance(
            api_res['result']['result'], expectdata['result']['result'])

        if diff > 10:
            #打印输出编辑距离
            print("\tDIFF: resultImg 不一致,编辑距离为{}".format(diff))

            print("\tDIFF: 返回信息对比结果 不一致")
            print("\t期望结果: {}".format(str(expectdata)))
            print("\t请求结果: {}".format(str(api_res)))
            status_report += "DIFF: message 不一致\n" + \
                             "期望结果: {}\n".format(str(expectdata)) + \
                             "请求结果: {}\n".format(str(api_res))
        else:
            status_report += "SUCC: 所有信息 一致\n"
            print("\tDIFF: result 不一致,编辑距离为{}".format(diff))
            print("编辑距离<10, 差异可接受, case通过\n")
            print(api_res['result']['result'])
            print(expectdata['result']['result'])
        # else:
        #     status_report += "DIFF: message 不一致\n" + \
        #                      "期望结果: {}\n".format(str(expectdata)) + \
        #                      "请求结果: {}\n".format(str(api_res))
        # print("\tDIFF: 返回信息对比结果 不一致")
        # print("\t期望结果: {}".format(str(expectdata)))
        
        # else:
        #     status_report += "DIFF: message 不一致\n" + \
        #                      "期望结果: {}\n".format(str(expectdata)) + \
        #                      "请求结果: {}\n".format(str(api_res))
        # print("\tDIFF: 返回信息对比结果 不一致")
        # print("\t期望结果: {}".format(str(expectdata)))
        # print("\t请求结果: {}".format(str(api_res)))
        # status_report += "DIFF: message 不一致\n" + \
        #                  "期望结果: {}\n".format(str(expectdata)) + \
        #                  "请求结果: {}\n".format(str(api_res))
    else:
        status_report += "SUCC: 所有信息 一致\n"
        print("SUCC: 所有信息 一致\n")
        print(api_res['result']['result'])
        print(expectdata['result']['result'])
        return status_report

        
def check_error_res(api_res, expectdata, status_report):
    if api_res == expectdata:
        status_report += "meaasge 内容与预期结果一致\n"
        print(api_res["message"])
    else:
        status_report += "meaasge 内容与预期结果不一致\n"
        print(api_res["message"])
    return status_report


def compare_res(api_res, saved_res, status_report):
    data_path = os.environ.get('API_DATA_PATH')
    expectdata_path = os.path.join(data_path,
        saved_res[0]["expectdata"])

    if not os.path.exists(expectdata_path):
        print("Error: 缺少验证数据 {}".format(expectdata_path))
        return None
    with open(expectdata_path, 'r') as f:
        expectdata = eval(f.read())

        # status_report = check_normal_res(status_report, api_res, expectdata)
        
        saved_report = check_normal_res(status_report, api_res, expectdata)
        # 接口返回结果没有 data json等字段，说明返回的是一个报警信息
        # elif "data" in ocr_res and ocr_res["data"] is None:

        # status_report += "不需要比对图片\n"
        # status_report = check_error_res(api_res, expectdata, status_report)
    return status_report


def compare_res_konwlages(api_res, saved_res, status_report):
    data_path = os.environ.get('DATA_PATH', '/app/data')
    expectdata_path = os.path.join(data_path, "resultresponse",
                                   saved_res["expectdata"])

    if not os.path.exists(expectdata_path):
        print("Error: 缺少验证数据 {}".format(expectdata_path))
        return None
    with open(expectdata_path, 'r') as f:
        expectdata = eval(f.read())

        # status_report = check_normal_res(status_report, api_res, expectdata)
        saved_report = check_normal_knowlageres(
            status_report, api_res, expectdata)
        # 接口返回结果没有 data json等字段，说明返回的是一个报警信息
        # elif "data" in ocr_res and ocr_res["data"] is None:

        # status_report += "不需要比对图片\n"
        # status_report = check_error_res(api_res, expectdata, status_report)
    return status_report
