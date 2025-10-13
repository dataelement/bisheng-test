import base64
import os
import requests

import pytest
import allure

from tests.confdata import CONFDATA


@allure.feature("bisheng-uns")
@allure.story("config")
@pytest.mark.skip
def test_uns_config():
    uns_ep = os.environ.get("TEST_UNSTRUCTURED_EP")
    rt_ep = os.environ.get("TEST_RT_EP")
    url = f"http://{uns_ep}/v1/config"
    resp = requests.get(url, json={}).json()
    assert 'pdf_model_params' in resp['config']
    for k, v in resp['config']['pdf_model_params'].items():
        assert rt_ep in v, f'config {k}:{v} is wrong' 



@allure.feature("bisheng-uns")
@allure.story("etl4llm.partition")
@pytest.mark.parametrize("file_type,args", CONFDATA.part_cases())
def test_part(file_type, args):
    filename = args['filename']
    uns_ep = os.environ.get("TEST_UNSTRUCTURED_EP")
    url = f"http://{uns_ep}/v1/etl4llm/predict"
    b64_data = base64.b64encode(open(filename, "rb").read()).decode()
    inp = dict(
        filename=os.path.basename(filename),
        b64_data=[b64_data],
        mode="partition",
        parameters={"start": 0, "n": 5},
    )
    resp = requests.post(url, json=inp).json()
    assert resp["status_code"] == 200, resp


@allure.feature("bisheng-uns")
@allure.story("etl4llm.topdf")
@pytest.mark.parametrize("file_type,args", CONFDATA.topdf_cases())
def test_any2pdf(file_type, args):
    filename = args['filename']
    uns_ep = os.environ.get("TEST_UNSTRUCTURED_EP")
    url = f"http://{uns_ep}/v1/etl4llm/predict"

    b64_data = base64.b64encode(open(filename, "rb").read()).decode()
    inp = dict(
        filename=os.path.basename(filename),
        b64_data=[b64_data],
        mode="topdf",
    )
    resp = requests.post(url, json=inp).json()
    assert resp["status_code"] == 200, resp
    assert len(resp["b64_pdf"]) > 7, 'b64_pdf data is less then 7 bytes'

    # out_fn = os.path.basename(filename).rsplit('.', 1)[0] + '.pdf'
    # out_file = os.path.join('./output/data', out_fn)
    # with open(ouf_file, 'wb') as fout:
    #     fout.write(base64.b64decode(resp['b64_pdf']))
