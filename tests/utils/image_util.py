import base64
import os


# 图片处理
def convert_b64(file):
    if os.path.isfile(file):
        with open(file, 'rb') as fh:
            x = base64.b64encode(fh.read())
            return x.decode('ascii').replace('\n', '')
    else:
        return None
