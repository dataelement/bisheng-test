import pytest
import base64
import copy
import json
import os
import time

import requests
import allure

class OCRClient(object):
    def __init__(self, **kwargs):
        url = kwargs.get('url')
        elem_ocr_collection_v3 = kwargs.get('model_name')
        self.ep = f'{url}/v2.1/models/{elem_ocr_collection_v3}/infer'
        self.client = requests.Session()
        self.timeout = kwargs.get('timeout', 10000)
        self.params = {
            'sort_filter_boxes': True,
            'enable_huarong_box_adjust': True,
            'rotateupright': False,
            'support_long_image_segment': True,
        }

        self.scene_mapping = {
            'print': {
                'det': 'general_text_det_mrcnn_v2.0',
                'recog': 'transformer-blank-v0.2-faster'
            },
            'hand': {
                'det': 'general_text_det_mrcnn_v2.0',
                'recog': 'transformer-hand-v1.16-faster'
            }
        }

    def predict(self, inp):
        scene = inp.pop('scene', 'print')
        b64_image = inp.pop('b64_image')
        params = copy.deepcopy(self.params)
        params.update(self.scene_mapping[scene])
        params.update(inp)
        req_data = {'param': params, 'data': [b64_image]}
        try:
            r = self.client.post(url=self.ep,
                                 json=req_data,
                                 timeout=self.timeout)
            return r.json()
        except Exception as e:
            return {'code': 400, 'message': str(e)}


@allure.feature("bisheng-rt-ent")
@allure.story("elem_ocr.load_infer_unload")
@pytest.mark.run(order=1)
def test_elem_ocr(ocr_model_info, elem_model_test_images, repo_models):
    name, load_params = ocr_model_info
    if name not in repo_models:
        print(f'model [{name}] not in repository, escape test')
        return

    RT_EP = os.environ.get('TEST_RT_EP')
    ep_prefix = f'http://{RT_EP}'
    repo_ep = f'http://{RT_EP}/v2/repository'
    headers = {'Content-type': 'application/json'}
    load_ep = f'{repo_ep}/models/{name}/load'
    unload_ep = f'{repo_ep}/models/{name}/unload'
    ready_ep = f'{ep_prefix}/v2/models/{name}/ready'

    print(f'load model {name}...')
    resp = requests.post(load_ep, json=load_params, headers=headers)
    assert resp.status_code == 200
    time.sleep(2)

    ready_resp = requests.get(ready_ep, json={}, headers=headers)
    assert ready_resp.status_code == 200

    succ = True
    try:
        print(f'infer with model {name}...')
        for f in elem_model_test_images:
            b64_data = base64.b64encode(open(f, 'rb').read()).decode()
            kwargs = {'model_name': name, 'url': ep_prefix}
            ocr_client = OCRClient(**kwargs)

            inp = {'b64_image':  b64_data}
            outp = ocr_client.predict(inp)
            print('elem ocr print result', outp)
            assert outp['code'] == 200, outp

            inp = {'b64_image':  b64_data, 'scene': 'hand'}
            outp = ocr_client.predict(inp)
            print('elem ocr hand result', outp)
            assert outp['code'] == 200, outp
    except Exception as e:
        succ = False
        print('err in infer:', e)
    finally:
        print(f'unload model {name} ...')
        resp = requests.post(unload_ep, json={}, headers=headers)
        assert resp.status_code == 200

        time.sleep(3)
        ready_resp = requests.get(ready_ep, json={}, headers=headers)
        assert ready_resp.status_code == 400
    
    assert succ, 'infer has execption'


@allure.feature("bisheng-rt-ent")
@allure.story("elem_layout.load_infer_unload")
@pytest.mark.run(order=2)
def test_elem_layout(layout_model_info, elem_model_test_images, repo_models):
    name, load_params = layout_model_info
    if name not in repo_models:
        print(f'model [{name}] not in repository, escape test')
        return

    RT_EP = os.environ.get('TEST_RT_EP')
    ep_prefix = f'http://{RT_EP}'
    repo_ep = f'http://{RT_EP}/v2/repository'
    headers = {'Content-type': 'application/json'}
    load_ep = f'{repo_ep}/models/{name}/load'
    unload_ep = f'{repo_ep}/models/{name}/unload'
    ready_ep = f'{ep_prefix}/v2/models/{name}/ready'
    layout_infer_ep = f'{ep_prefix}/v2.1/models/elem_layout_v1/infer'
    table_infer_ep = f'{ep_prefix}/v2.1/models/elem_table_detect_v1/infer'

    print(f'load model {name}...')
    resp = requests.post(load_ep, json=load_params, headers=headers)
    assert resp.status_code == 200
    time.sleep(2)

    ready_resp = requests.get(ready_ep, json={}, headers=headers)
    assert ready_resp.status_code == 200

    succ = True
    try:
        print(f'infer with model {name}...')
        for f in elem_model_test_images:
            b64_data = base64.b64encode(open(f, 'rb').read()).decode()
            inp = {'b64_image': b64_data}
            outp = requests.post(layout_infer_ep, json=inp).json()
            print('layout infer result', outp)
            assert outp is not None

            outp = requests.post(table_infer_ep, json=inp).json()
            print('table infer result', outp)
            assert outp is not None
    except Exception as e:
        succ = False
        print('err in infer:', e)
    finally:
        print(f'unload model {name} ...')
        resp = requests.post(unload_ep, json={}, headers=headers)
        assert resp.status_code == 200

        time.sleep(3)
        ready_resp = requests.get(ready_ep, json={}, headers=headers)
        assert ready_resp.status_code == 400

    assert succ, 'infer has execption'
