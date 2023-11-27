import pytest
import configparser
import os
import requests
import json

from tests.utils.yaml_util import FromYaml2Json, read_yaml


@pytest.fixture(scope="session", autouse=True)
def set_env():
    config_path = './config/global.ini'
    config = configparser.ConfigParser()
    config.read_file(open(config_path))
    for k, v in config.items("DEFAULT"):
        k_ = k.upper()
        if k_ not in os.environ:
            os.environ[k_] = v


@pytest.fixture
def knowledge_cases():
    yaml_file = os.environ.get('BISHENG_KNOWLAGEQA')
    data = FromYaml2Json(yaml_file)
    data_item = data['cases'] # [dict, dict]
    return data_item


@pytest.fixture
def login_cases():
    yaml_file = os.environ.get('BISHENG_LOGIN')
    data = FromYaml2Json(yaml_file)
    data_item = data['cases']  # [dict(), dict()]
    return data_item


@pytest.fixture
def regist_cases():
    yaml_file = os.environ.get('BISHENG_REGIST')
    data = FromYaml2Json(yaml_file)
    data_item = data['cases']  # [dict(), dict()]
    return data_item


@pytest.fixture
def uns_cases():
    yaml_file = os.environ.get('BISHENG_UNSTRUCTURED')
    data = FromYaml2Json(yaml_file)
    data_item = data['cases'] 
    return data_item


@pytest.fixture
def ocr_model_info():
    case_file = os.environ.get('RT_CLOSE_MODEL')
    config = json.load(open(case_file))
    models = config['models'] 
    params = config['load_params']
    gpus = os.environ.get('TEST_RT_GPU')
    instance_groups = f"device=gpu;gpus={gpus}"
    for model, param in zip(models, params):
        if model == 'elem_ocr_collection_v3':
            param["parameters"]["instance_groups"] = instance_groups
            return (model, param)


@pytest.fixture
def layout_model_info():
    case_file = os.environ.get('RT_CLOSE_MODEL')
    config = json.load(open(case_file))
    models = config['models'] 
    params = config['load_params']
    gpus = os.environ.get('TEST_RT_GPU')
    instance_groups = f"device=gpu;gpus={gpus}"
    for model, param in zip(models, params):
        if model == 'elem_layout_collection_v1':
            param["parameters"]["instance_groups"] = instance_groups
            return (model, param)


@pytest.fixture
def elem_model_test_images():
    case_file = os.environ.get('RT_CLOSE_MODEL')
    config = json.load(open(case_file))
    return config['test_images']


@pytest.fixture
def testing_llm_model():
    return os.environ.get('TESTING_LLM_MODEL')


@pytest.fixture
def repo_models():
    RT_EP = os.environ.get('TEST_RT_EP')
    repo_ep = f'http://{RT_EP}/v2/repository/index'
    result = requests.post(repo_ep, json={}).json()
    model_map = {}
    for info in result:
        model_map[info['name']] = 1 

    return model_map

