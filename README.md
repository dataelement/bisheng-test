## BISHENG API接口自动化

Bisheng-test is an sub-module of bisheng projects. It contains all test cases for
the bisheng projects

## 目录结构说明
| 文件夹/文件             | 内容                            | 说明                                                           |
|--------------------|-------------------------------|--------------------------------------------------------------|
| cofig              | 接口入参配置                        | 根据不同的模块创建不同文件夹，再配置test_***.yaml文件                            |
| data/test_data     | 入参所需要的文件合集                    | eg: 知识库上传文件                                                  |                     |
| data/response_data | 所有接口的返回数据落盘                   | 根据不同模块创建不同文件，落盘文件以txt格存储                                     |
| docker             | 基于 Docker 的 Python Web 应用测试环境 | 启动了一个 Docker 容器                                              |
| output             | logs存储                        | 测试执行后产出的log                                                  |
| scripts            | 启动脚本,定义了一个 Docker 容器的运行命令     | 启动一个rt容器                                                     |
| tests/testcases    | 测试脚本文件夹                       | 根据不同的模块创建不同文件夹，注意命名要清晰                                       |
| tests/utils        | 封装好的函数、工具等                    | 根据不同的模块创建不同文件夹，注意命名要清晰                                       |



## repo文件说明
* `cofig/global.ini`：主要的配置路径，可以配置数据路径、镜像名、配置文件路径、ip等
* `scripts/prepare.sh`: 启动RT容器的脚本（新版本已经没有RT服务了）
* `setup.py`:Python 打包配置文件，用于将您的测试框架 bisheng-test打包成一个可以通过 pip install安装的 Python 包
* `tests/conftest.py`:pytest 测试框架的 fixture 定义文件，主要用于为测试用例提供各种测试数据和环境配置
* `tests/confdata.py`:测试数据配置中心，用于集中管理和提供各种类型的测试数据和配置信息
* `run_test.py`:测试程序启动代码

## Quick start
1. 新建py文件
2. 准备测试数据yaml文件， 在ini文件中配置测试数据路径
