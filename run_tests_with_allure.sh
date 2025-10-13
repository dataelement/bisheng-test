#!/bin/bash

echo "🚀 开始运行测试，并生成 Allure 数据..."
pytest \
  --alluredir=./allure-results \
  -n 8 \
  --dist=load \
  --timeout=600 \
  tests/testcases/

echo "📊 生成 Allure HTML 报告..."
allure generate ./allure-results -o ./allure-report --clean

echo "🔗 打开 Allure 报告..."
allure open ./allure-report