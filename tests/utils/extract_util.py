# flake8: noqa

import re

from tests.utils.exception_utils import exception_utils
from tests.utils.text_util import extract_txt, read_txt
from tests.utils.yaml_util import read_yaml

DATA_PATH = os.environ.get('DATA_PATH', '/app/data')


@exception_utils
def extract_util(case_file,
        extract_yamlfile=None,
        default_yamlfile=None):
    """
    数据关联的公共方法,支持模板数据，yaml数据联合excel数据
    思路:
    1.运行用例前，检查用例yaml中是否有${}
    2.有，则检查${}中的变量是否存在于extract.yaml中
    3.有，则替换；无，则不变，或设置默认值
    4.内存中覆盖yaml中读取的值
    5.再进行数据驱动
    返回——>替换${变量}后的数据
    """

    if extract_yamlfile is None:
        extract_yamlfile = (
            "%s/data_driven_yaml/extract.yaml" % DATA_PATH)

    if default_yamlfile is None:
        default_yamlfile = (
            "%s/data_driven_yaml/default_variable.yaml" % DATA_PATH)

    # 运行用例
    text_file = '%s/extract_replace.txt' % DATA_PATH

    # 运行前先清空extract.txt
    # truncate_txt(text_file)

    # 1.返回全部匹配到的结果，且去重
    value_cases = str(read_yaml(case_file))
    # 一.写入txt
    extract_txt(
        text_file='%s/extract_replace.txt' % DATA_PATH, data=value_cases)

    p = r'\$\{(.*?)\}'
    match_list = list(set(re.findall(p, value_cases)))

    # 2.提取字段的key列表(关联变量 和 用户默认变量，将他们合并)
    global value_extract_keys, value_extract
    if read_yaml(extract_yamlfile):
        value_extract = read_yaml(extract_yamlfile)
        vlaue_default_variable = read_yaml(default_yamlfile)
        value_extract.update(vlaue_default_variable)
        value_extract_keys = list(value_extract.keys())
        # print(value_extract)
    else:
        print("extract.yaml文件中没有储存的变量")
        if read_yaml(default_yamlfile):
            vlaue_default_variable = read_yaml(default_yamlfile)
            value_extract_keys = list(vlaue_default_variable.keys())

    # todo: naive logic: 每次结果存入txt文件，然后再每次读取txt文件, 待改进
    # 3.动态替换${}
    for m in match_list:
        if m in value_extract_keys:
            p1 = r'\${%s}' % m
            # 替换${}中内容
            replace = re.sub(p1, value_extract[m], read_txt(text_file))
            # 三.每次覆盖动态写入
            extract_txt(text_file=text_file, data=replace)
        else:
            print("关联数据中，没有该key：%s" % m)

    return eval(read_txt(text_file))['cases']


def save_variable(key, value):
    """保存变量到extract.yaml文件，需要模块运行前先进行清空"""
    # 1.数据按格式追加写入extract_save.txt文件

    file = '%s/data/extract_save.txt' % DATA_PATH
    extract_yamlfile = "%s/data/data_driven_yaml/extract.yaml" % DATA_PATH
    write_txt(file, '"%s":"%s",' % (key, value))
    variable = eval("{%s}" % read_txt(file)[0:-1])
    write_yaml(data=variable, yaml_file=extract_yamlfile)


# 测试数据关联返回数据
if __name__ == '__main__':
    cases_file = './data/case_bisheng/case1_general_template.yaml'
    extract_file = './data/data_driven_yaml/extract.yaml'
    rep = extract_util(cases_file, extract_file)
    print(rep)

