# flake8: noqa
import os

def read_txt(text_file):
    """读取txt文件"""
    with open(text_file, 'r', encoding='utf-8') as f:
        return f.read()


def write_txt(text_file, data):
    """追加写入txt文件"""
    with open(text_file, 'a') as f:
        f.write(data)


def extract_txt(text_file, data):
    """覆盖写入txt文件"""
    # 覆盖保存
    with open(text_file, 'w+') as f:
        f.write(data)
    # 读取
    # return read_txt(text_file)


def truncate_txt(text_file):
    """清空txt文件"""
    with open(text_file, 'w') as f:
        f.truncate()


def read_txt_handel(text_file=None):
    """将保存运行结果的txt数据，处理成想要的格式"""
    if text_file is None:
        text_file = os.environ.get('TEXT_FILE', '/app/output/run_result.txt')

    value = read_txt(text_file=text_file)
    l_reponse = []
    l_ispass = []
    for i in value[0:-1].split("|"):
        l_reponse.append(i.split('__')[0])
        l_ispass.append(i.split('__')[1])

    # print(l_reponse)
    # print(l_ispass)

    return l_reponse, l_ispass


if __name__ == '__main__':
    read_txt_handel()
