import configparser
import os
import json

from tests.utils.yaml_util import read_yaml


class ConfData(object):
    # def __init__(self):
    #     self.config_dict = None
    #     config_path = './config/global.ini'
    #     config = configparser.ConfigParser()
    #     config.read_file(open(config_path))
    #     self.config_dict = {}
    #     for k, v in config.items("DEFAULT"):
    #         k_ = k.upper()
    #         self.config_dict[k_] = os.environ.get(k_, v)
    #
    #     print("ConfData 的所有键:", self.config_dict.keys())  # 正确：使用 self
    #     print("TEST_BISHENG_EP（来自 ConfData）:", self.config_dict.get('TEST_BISHENG_EP'))
    #
    #     self.config_dict = self.config_dict
    # print("TEST_BISHENG_EP 的值:", os.environ.get('TEST_BISHENG_EP'))
    def __init__(self):
        """从 global.ini 读取配置并设置到环境变量（如果尚未设置）"""
        self.config_dict = {}

        # 1. 读取配置文件
        config_path = './config/global.ini'
        config = configparser.ConfigParser()
        config.read_file(open(config_path))

        # 2. 处理DEFAULT部分的配置项
        for key, value in config.items("DEFAULT"):
            env_key = key.upper()  # 转换为大写作为环境变量名

            # 如果环境变量未设置，则使用ini文件中的值
            if env_key not in os.environ:
                os.environ[env_key] = value
                # print(f"已从ini文件设置环境变量: {env_key}={value}")

            # 将配置存入config_dict（优先使用环境变量的值）
            self.config_dict[env_key] = os.environ.get(env_key, value)

    def part_cases(self):
        yaml_file = self.config_dict.get('BISHENG_UNSTRUCTURED_CASE2')
        config = read_yaml(yaml_file)
        return [(v['type'], dict(filename=v['file']))
                for v in config['part_files']]

    def topdf_cases(self):
        yaml_file = self.config_dict.get('BISHENG_UNSTRUCTURED_CASE2')
        config = read_yaml(yaml_file)
        return [(v['type'], dict(filename=v['file']))
                for v in config['topdf_files']]

    def llm_cases(self):
        case_file = self.config_dict.get('RT_LLM_MODEL')
        config = json.load(open(case_file))
        models = config['models']
        params = config['load_params']
        gpus = self.config_dict.get('TEST_RT_LLM_GPU')

        infos = []
        instance_groups = f"device=gpu;gpus={gpus}"
        for model, param in zip(models, params):
            param["parameters"]["instance_groups"] = instance_groups
            infos.append((model, param))

        return infos

    def emb_cases(self):
        case_file = self.config_dict.get('RT_EMB_MODEL')
        config = json.load(open(case_file))
        models = config['models']
        params = config['load_params']
        gpus = self.config_dict.get('TEST_RT_GPU')

        infos = []
        instance_groups = f"device=gpu;gpus={gpus}"
        for model, param in zip(models, params):
            param["parameters"]["instance_groups"] = instance_groups
            infos.append((model, param))

        return infos


    def login_cases(self):
        yaml_file = self.config_dict.get('BISHENG_LOGIN')
        config = read_yaml(yaml_file)
        cases = config['case_groups']

        infos = []
        for case in zip(cases):
            infos.append(case)

        return infos

    def regist_cases(self):
        yaml_file = self.config_dict.get('BISHENG_REGIST')
        config = read_yaml(yaml_file)
        cases = config['case_groups']

        infos = []
        for case in zip(cases):
            infos.append(case)

        return infos

    def knowledge_cases(self):
        yaml_file = self.config_dict.get('BISHENG_KNOWLEDGE')
        config = read_yaml(yaml_file)
        cases = config['case_groups']

        infos = []
        for case in zip(cases):
            infos.append(case)

        return infos

    def knowledgeqa_cases(self):
        yaml_file = self.config_dict.get('BISHENG_KNOWLEDGEQA')
        config = read_yaml(yaml_file)
        cases = config['case_groups']

        infos = []
        for case in zip(cases):
            infos.append(case)

        return infos
    #单文档问答
    def singledocument_cases(self):
        yaml_file = self.config_dict.get('BISHENG_SINGLEDOCUMENT')
        config = read_yaml(yaml_file)
        cases = config['case_groups']

        infos = []
        for case in zip(cases):
            infos.append(case)

        return infos

    def rolelist_cases(self):
        yaml_file = self.config_dict.get('BISHENG_ROLELIST')
        config = read_yaml(yaml_file)
        cases = config['case_groups']

        infos = []
        for case in zip(cases):
            infos.append(case)

        return infos

    def role_cases(self):
        yaml_file = self.config_dict.get('BISHENG_ROLE')
        config = read_yaml(yaml_file)
        cases = config['case_groups']
        print("=======",cases)
        infos = []
        for case in zip(cases):
            infos.append(case)
        return infos
        # return cases

    def role_deletecases(self):
        yaml_file = self.config_dict.get('BISHENG_ROLE_DELETE')
        config = read_yaml(yaml_file)
        cases = config['case_groups']
        infos = []
        for case in zip(cases):
            infos.append(case)
        return infos

CONFDATA = ConfData()
