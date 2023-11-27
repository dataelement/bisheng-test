import configparser
import os
import json

from tests.utils.yaml_util import read_yaml


class ConfData(object):
    def __init__(self):
        config_path = './config/global.ini'
        config = configparser.ConfigParser()
        config.read_file(open(config_path))
        config_dict = {}
        for k, v in config.items("DEFAULT"):
            k_ = k.upper()
            config_dict[k_] = os.environ.get(k_, v)

        self.config_dict = config_dict

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


CONFDATA = ConfData()
