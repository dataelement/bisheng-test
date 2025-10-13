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


def check_normal_code(status_report, api_res, expectdata):
    if str(api_res['status_code']) != str(expectdata['status_code']):

        # 比较api_res里边result的diff，如果编辑距离<10，则认为相等
        diff = Levenshtein.distance(
            api_res['data'], expectdata['data'])

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
            print(api_res['data']['result']['answer'])
            print(expectdata['data']['result']['answer'])
    else:
        status_report += "SUCC: 所有信息 一致\n"
        print("👏SUCC: 所有信息 一致\n")
        print("\t期望结果: {}".format(str(expectdata)))
        print("\t请求结果: {}".format(str(api_res)))

        # print(api_res['data']['result']['answer'])
        # print(expectdata['data']['result']['answer'])
        return status_report

        
def check_error_res(api_res, expectdata, status_report):
    if api_res == expectdata:
        status_report += "meaasge 内容与预期结果一致\n"
        print(api_res["message"])
    else:
        status_report += "meaasge 内容与预期结果不一致\n"
        print(api_res["message"])
    return status_report


# def compare_res(api_res, saved_res, status_report):
#     # 判断expectresult 是否与请求的接口返回结果一致
#     if saved_res[0]["expectresult"]["status_code"] != api_res["status_code"]:
#         status_report += "接口返回结果与expectresult不一致\n"
#         raise Exception(u"请求异常")

#     else:
#         data_path = os.environ.get('API_DATA_PATH')
#         expectdata_path = os.path.join(data_path,
#         saved_res[0]["expectdata"])
#         if not os.path.exists(expectdata_path):
#             print("Error: 缺少验证数据 {}".format(expectdata_path))
#             return None
#         with open(expectdata_path, 'r') as f:
#             expectdata = eval(f.read())
#             saved_report = check_normal_res(status_report, api_res, expectdata)
    
#     return status_report
def compare_res(api_res, saved_res, status_report):
    # expect_result = saved_res[0]["expectdata"]
    # print("expect_result"+ expect_result)
    # if (expect_result.get("status_code") and expect_result["status_code"] != api_res["status_code"]):
    #     status_report += "接口返回结果与expectresult不一致\n"
    #     raise Exception(u"请求异常")
        
    data_path = os.environ.get('API_DATA_PATH')
    expectdata_file = saved_res[0].get("expectdata")
    if expectdata_file:
        expectdata_path = os.path.join(data_path, expectdata_file)
        if not os.path.exists(expectdata_path):
            print("Error: 缺少验证数据 {}".format(expectdata_path))
            return None
        with open(expectdata_path, 'r') as f:
            expectdata = eval(f.read())
            # print("expectdata"+expectdata)
            status_report = check_normal_res(status_report, api_res, expectdata)
    return status_report


def compare_res_code(api_res, saved_res, status_report):
    data_path = os.environ.get('API_DATA_PATH')
    expectdata_file = saved_res[0].get("expectdata")
    if expectdata_file:
        expectdata_path = os.path.join(data_path, expectdata_file)
        if not os.path.exists(expectdata_path):
            print("Error: 缺少验证数据 {}".format(expectdata_path))
            return None
        with open(expectdata_path, 'r') as f:
            # expectdata = eval(f.read())
            expectdata = json.load(f)
            # print("expectdata" + expectdata)
            status_report = check_normal_code(status_report, api_res, expectdata)
    return status_report
    # if not os.path.exists(expectdata_path):
    #     print("Error: 缺少验证数据 {}".format(expectdata_path))
    #     return None
    # with open(expectdata_path, 'r') as f:
    #     expectdata = eval(f.read())

    #     # status_report = check_normal_res(status_report, api_res, expectdata)
    #     saved_report = check_normal_knowlageres(
    #         status_report, api_res, expectdata)
    #     # 接口返回结果没有 data json等字段，说明返回的是一个报警信息
    #     # elif "data" in ocr_res and ocr_res["data"] is None:

    #     # status_report += "不需要比对图片\n"
    #     # status_report = check_error_res(api_res, expectdata, status_report)
    # return status_report
# def check_normal_res(status_report, api_res, expectdata):
#     if str(api_res) != str(expectdata):
#         print("\tDIFF: 返回信息对比结果 不一致")
#         print("\t期望结果: {}".format(str(expectdata)))
#         print("\t请求结果: {}".format(str(api_res)))
#         status_report += "DIFF: message 不一致\n" + \
#                          "期望结果: {}\n".format(str(expectdata)) + \
#                          "请求结果: {}\n".format(str(api_res))
#     else:
#         status_report += "SUCC: 所有信息 一致\n"
#         print("SUCC: 所有信息 一致\n")
#         return status_report