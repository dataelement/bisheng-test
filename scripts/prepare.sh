#!/bin/bash

function prepare() {
    pip_repo="https://mirrors.tencent.com/pypi/simple"
    pip3 install -r requirements.txt -i $pip_repo
}


function run_rt005_demo_docker() {
  LOCAL_MODEL_REPO="/home/public/llm"
  MAPING_MODEL_REPO="/opt/bisheng-rt/models/model_repository"
  MOUNT="-v $LOCAL_MODEL_REPO:$MAPING_MODEL_REPO -v $HOME:$HOME"
  IMAGE="dataelement/bisheng-rt:0.0.5"
  docker run -itd --gpus all -p 9000:9000 -p 9001:9001 -p 9002:9002 --shm-size=16g \
    --ulimit memlock=-1 --ulimit stack=67108864  --workdir /opt/bisheng-rt \
    --name bisheng_rt_v005_demo ${MOUNT} $IMAGE \
    bash bin/entrypoint.sh --serveraddr=192.168.106.7
}


function start_test_rt_docker() {
  LOCAL_MODEL_REPO="/home/public/llm"
  MAPING_MODEL_REPO="/opt/bisheng-rt/models/model_repository"
  DEVICES='"device=6,7,8"'
  MOUNT="-v $LOCAL_MODEL_REPO:$MAPING_MODEL_REPO -v $HOME:$HOME -v /public:/public"
  IMAGE="dataelement/bisheng-rt:0.0.5"
  docker run -itd --gpus ${DEVICES} -p 6601:9001 -p 6602:9002 --shm-size=16g \
    --ulimit memlock=-1 --ulimit stack=67108864  --workdir /opt/bisheng-rt \
    --name bisheng_rt_v005_test_hf ${MOUNT} $IMAGE \
    bash bin/entrypoint.sh --serveraddr=192.168.106.7
}


function run_test() {
    # unset http_proxy
    # unset https_proxy
    # unset HTTPS_PROXY
    # unset HTTP_PROXY
    # python3 -m pytest ./tests/testcases/bisheng_uns

    TEST_RT_EP=192.168.106.12:6601 python3 \
        -m pytest ./tests/testcases/bisheng_rt/test_close_model.py
}

# run_rt005_demo_docker
start_test_rt_docker
# run_rt_docker
# prepare
# run_test
