import pytest
import copy
import os
import time

import requests
import allure

from tests.confdata import CONFDATA


def call_emb(model, ep):
    input_template = {
      'model': 'unknown',
      "texts": ["how much protein should a female eat"],
      "type": "query"
    }
    payload = copy.copy(input_template)
    payload['model'] = model
    response = requests.post(url=ep, json=payload).json()
    embeddings = response.get('embeddings', [])
    assert embeddings, response


@allure.feature("bisheng-rt")
@allure.story("emb_model.load_infer_unload")
@pytest.mark.parametrize("name,params", CONFDATA.emb_cases())
def test_emb_models(name, params, repo_models):
    RT_EP = os.environ.get('TEST_RT_EP')
    ep_prefix = f'http://{RT_EP}'
    repo_ep = f'http://{RT_EP}/v2/repository'
    headers = {'Content-type': 'application/json'}
    if name not in repo_models:
        print(f'model [{name}] not in repository, escape test')
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
        call_emb(name, infer_ep)
    except Exception as e:
        pritn('infer has execption', e)
        succ = False
    finally:
        print(f'unload model {name} ...')
        resp = requests.post(unload_ep, json={}, headers=headers)
        assert resp.status_code == 200

        time.sleep(3)
        ready_resp = requests.get(ready_ep, json={}, headers=headers)
        assert ready_resp.status_code == 400

    assert succ, 'infer has execption'
