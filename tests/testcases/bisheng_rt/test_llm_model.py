import pytest
import copy
import os
import time

import requests
import allure

from tests.confdata import CONFDATA


def call_llm(model, ep):
    input_template = {
      'model': 'unknown',
      'messages': [
        {'role': 'system', 'content': ''},
        {
          'role': 'user', 
          'content': '以“今晚夜色真美”为开头写一篇短文，包含悬疑元素'}],
      'max_tokens': 256
    }
    payload = copy.copy(input_template)
    payload['model'] = model
    response = requests.post(url=ep, json=payload).json()
    print('llm response', response)
    choices = response.get('choices', [])
    assert choices, response


@allure.feature("bisheng-rt")
@allure.story("llm_model.load_infer_unload")
@pytest.mark.parametrize("name,params", CONFDATA.llm_cases())
def test_llm_models(name, params, repo_models, testing_llm_model):
    RT_EP = os.environ.get('TEST_RT_EP')
    ep_prefix = f'http://{RT_EP}'
    repo_ep = f'http://{RT_EP}/v2/repository'
    headers = {'Content-type': 'application/json'}
    if name not in repo_models:
        print(f'model [{name}] not in repository, escape test')
        return

    if testing_llm_model and name != testing_llm_model:
        print(f'use set the specific model by TESTING_LLM_MODEL, escape other')
        return

    load_ep = f'{repo_ep}/models/{name}/load'
    unload_ep = f'{repo_ep}/models/{name}/unload'
    ready_ep = f'{ep_prefix}/v2/models/{name}/ready'
    infer_ep = f'{ep_prefix}/v2.1/models/{name}/infer'

    print(f'load model {name}...')
    resp = requests.post(load_ep, json=params, headers=headers)
    assert resp.status_code == 200
    time.sleep(2)

    ready_resp = requests.get(ready_ep, json={}, headers=headers)
    assert ready_resp.status_code == 200

    succ = True
    try:
        print(f'infer with model {name}...')
        call_llm(name, infer_ep)
    except Exception as e:
        print('infer has execption', e)
        succ = False
    finally:
        print(f'unload model {name} ...')
        resp = requests.post(unload_ep, json={}, headers=headers)
        assert resp.status_code == 200

        time.sleep(3)
        ready_resp = requests.get(ready_ep, json={}, headers=headers)
        assert ready_resp.status_code == 400

    assert succ, 'infer has execption'
