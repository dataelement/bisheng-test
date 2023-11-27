FROM python:3.10-slim

ARG ALLURE_REPO=https://open:EFgg0jMqfE1rbw6b@nx.dataelem.com/repository/raw-hosted/packages
ARG BISHENG_TEST_VER=0.0.1
ARG ALLURE_RELEASE=2.24.1

ENV http_proxy=
ENV https_proxy=
ENV HTTPS_PROXY=
ENV HTTP_PROXY=

# RUN apt update && apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6 libgl1
RUN apt update && apt install -y curl unzip openjdk-17-jre locales vim
RUN python -m pip install --upgrade pip

# Configure language
RUN localedef -i en_US -f UTF-8 en_US.UTF-8
RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

COPY ./docker/deps/allure-${ALLURE_RELEASE}.zip /tmp/allure-${ALLURE_RELEASE}.zip
RUN unzip -q /tmp/allure-${ALLURE_RELEASE}.zip -d /opt/ && \
  chmod -R +x /opt/allure-$ALLURE_RELEASE/bin && \
  ln -s /opt/allure-$ALLURE_RELEASE/bin/allure /usr/bin/allure

# RUN curl ${ALLURE_REPO}/allure-${ALLURE_RELEASE}.zip \
#   -L -o /tmp/allure-${ALLURE_RELEASE}.zip && \
#  unzip -q /tmp/allure-${ALLURE_RELEASE}.zip -d /opt/ && \
#  chmod -R +x /opt/allure-$ALLURE_RELEASE/bin && \
#  ln -s /opt/allure-$ALLURE_RELEASE/bin/allure /usr/bin/allure

RUN mkdir /app
WORKDIR /app

# Clean caches
RUN apt-get clean && rm -rf /var/lib/apt/lists/* && rm -rf /root/.cache/pip && rm -fr /tmp/*
