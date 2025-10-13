import os
import requests


def test_repo_index():
    RT_EP = os.environ.get('TEST_RT_EP')
    repo_ep = f'http://{RT_EP}/v2/repository/index'
    result = requests.post(repo_ep, json={}).json()
    assert result, 'model not exsited'
