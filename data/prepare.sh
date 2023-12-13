#!/bin/bash

curr=$(cd $(dirname $0)/..; pwd)
cp -fr /public/bisheng/bisheng-test-data/rt_data ${curr}/data/
cp -fr /public/bisheng/bisheng-test-data/uns_data ${curr}/data/
cp -fr /public/bisheng/bisheng-test-data/response_data/login_data ${curr}/data/
# cp -fr /Users/sara/Desktop/DataElem/dev/bisheng-test/data/login_data ${curr}/data/

rm -fr ${curr}/data/allure-results/*
rm -fr ${curr}/data/default-reports/*
