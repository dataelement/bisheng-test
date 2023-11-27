# flake8: noqa
from functools import wraps
from pathlib import Path
import yaml
import json

import csv
import jinja2
from yaml.loader import SafeLoader

from tests.utils.excel_util import ExcelUtil

csv.field_size_limit(500 * 1024 * 1024)


def exception(fun):
    """异常处理额装饰器"""
    @wraps(fun)  # 这个可以用来返回原函数信息
    def wrapped_function(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except Exception as e:
            print("操作yaml文件出现异常：", e)
    return wrapped_function


@exception
def read_yaml(yaml_file):
    """读取yaml"""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        value = yaml.load(f, Loader=yaml.FullLoader)
        # print(value)
        return value


@exception
def write_yaml(data, yaml_file):
    """写yaml"""
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(
            data=data, stream=f, allow_unicode=True,
            sort_keys=False, default_flow_style=False)


@exception
def truncate_yaml(yaml_file):
    """清空yaml"""
    with open(yaml_file, 'w') as f:
        f.truncate()

@exception
def compose_yaml(yaml_temp_path, json_data_path):
    """templatepath中变量替换，替换参数在jsonpath以key-value形式表现"""

    with open(yaml_temp_path, encoding="utf-8") as w:
        string_var = w.read()
        new_data = json.load(open(json_data_path, 'r'))
        # jinjia2返回类型为String
        response = jinja2.Template(string_var).render(new_data)
        retult = yaml.safe_load(response)
        # print(type(retult['cases'][0]))
        """"返回result为一个list列表，list列表中包含多个字典，每个字典是一条用例"""
        return retult


@exception
def handler():
    """根据读取excel数据，生成yaml的测试用例数据"""
    output_path = os.environ.get('OUTPUT_PATH', '/app/output')
    file = "%s/data/case_excel/测试用例.xlsx" % output_path
    value, smoke = ExcelUtil(file).read_excel()
    sheet_names = ExcelUtil(file).wb.sheetnames
    n = 0
    j = 0  # 用例数
    # 1.写入全部的用例
    for sheet in sheet_names:
        data = value[n]
        print("%s模块中用例数：%s" % (sheet, len(data['cases'])))
        j += len(data['cases'])
        file = '%s/data/case_yaml/%s.yaml' % (output_path, sheet)
        write_yaml(data=data, yaml_file=file)
        n += 1
    return j


@exception
def FromYaml2Json(yaml_file):
    returnDict = {"cases": []}
    with open(yaml_file, encoding="utf-8") as f:
        cont_json = yaml.load(f, Loader=SafeLoader)
    returnDict['cases'] = cont_json
    return returnDict

