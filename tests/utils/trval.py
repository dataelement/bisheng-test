import json
import time
import os
import sys

from subprocess import PIPE, Popen

def writejson(jsonfile,jsoncontent):
    with open(jsonfile,'w') as f:
        json.dump(jsoncontent, f, ensure_ascii=False, indent=2)

def readjson(jsonfile):
    with open(jsonfile, 'r') as f:
        jsoncontent = json.load(f)
    return jsoncontent

def exec_cmd_in_docker(container, cmd):
    # https://blog.csdn.net/weixin_43628593/article/details/104860114
    s= os.system("docker exec %s %s"%(container, cmd))
    return s


def write_string(path, platform, string):
    with open(
        os.path.join(
            os.path.dirname(path),
            "{}_autotrval_res".format(platform) + 
            time.strftime("_%Y_%m_%d_%H_%M_%S", time.localtime()) + ".txt"),
        'w') as f:
        f.write(string)

def data_check(case_num, data):

    datapath = data[case_num]["datapath"]
    product_path = data[case_num]["outpath"]
    datapath = os.path.realpath(datapath)

    if not os.path.exists(os.path.join(datapath,"Images")) or \
        not os.path.exists(os.path.join(datapath,"Labels")):
        print("Error: 数据路径有误, 该路径下没有Images或Labels文件夹 \n")
        # sys.exit(1)
        return None,None

    product_path = os.path.realpath(product_path)
    if not os.path.exists(product_path):
        os.mkdir(product_path)
    return datapath,product_path
