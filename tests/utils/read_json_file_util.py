# coding=utf-8
import json
import os


class ReadJsonFileUtils:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = self.get_data()

    def get_data(self):
        fp = open(self.file_name, encoding='utf-8')
        data = json.load(fp)
        fp.close()
        return data

    def get_value(self, id):
        return self.data[id]

    @staticmethod
    def get_data_path(folder, fileName):
        # 数据目录从环境变量获取
        data_path = os.environ.get('DATA_PATH', '/app/data')
        data_file_path = os.path.join(data_path, folder, fileName)
        return data_file_path

