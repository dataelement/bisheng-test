#!/bin/bash


function create_test_dev() {
  MOUNT="-v $HOME:$HOME -v /public:/public"
  IMAGE="dataelement/bisheng-test-base:0.0.1"
  CNT="bisheng_test_dev001"
  docker run -p 5252:5252 --rm -itd --name ${CNT} ${MOUNT} $IMAGE bash
}


function test_build_image() {
  # install deps for opencv
  apt update && apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6 libgl1
  apt install -y curl unzip openjdk-17-jre
  python -m pip install --upgrade pip

  ALLURE_REPO=https://open:EFgg0jMqfE1rbw6b@nx.dataelem.com/repository/raw-hosted/packages
  BISHENG_TEST_VER=0.0.1
  ALLURE_RELEASE=2.24.1

  # install allure
  unzip -q /home/hanfeng/tars/allure-${ALLURE_RELEASE}.zip -d /opt/

  # curl ${ALLURE_REPO}/allure-${ALLURE_RELEASE}.zip \
  #   -L -o /tmp/allure-${ALLURE_RELEASE}.zip && \
  #   unzip -q allure-${ALLURE_RELEASE}.zip -d /opt/ && \
  #   chmod -R +x /opt/allure-$ALLURE_RELEASE/bin

  ln -s /opt/allure-$ALLURE_RELEASE/bin/allure /usr/bin/allure
  mkdir /app
}

function test_run() {
  python3 -m pytest -s -v ./tests --alluredir /app/data/allure-results
  allure generate /app/data/allure-results -o /app/data/default-reports --clean
  # allure open -h 0.0.0.0 -p 5252 /app/data/default-reports
  allure server -h 0.0.0.0 -p 5251 /app/data/default-report
}


function build_base_image() {
  docker build -t dataelement/bisheng-test-base:0.0.1 -f docker/base.Dockerfile .
}


function build_test_image() {
  docker build -t dataelement/bisheng-test:0.0.1 -f docker/Dockerfile .
}


function run_test_image() {
  MOUNT="-v $HOME:$HOME -v /public:/public"
  IMAGE="dataelement/bisheng-test:0.0.1"
  CNT="bisheng_test_v001"
  docker run -p 5252:5252 --rm -itd --name ${CNT} ${MOUNT} $IMAGE
}


# build_base_image
# create_test_dev
# build_test_image
run_test_image


