FROM dataelement/bisheng-test-base:0.0.1
MAINTAINER "Dataelem inc."

# unset proxy
ENV http_proxy=
ENV https_proxy=
ENV HTTP_PROXY=
ENV HTTPS_PROXY=

ARG PIP_REPO=https://mirrors.tencent.com/pypi/simple
RUN apt update && apt-get install -y nginx vim

# Configure language
RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
RUN localedef -i en_US -f UTF-8 en_US.UTF-8

# Prepare env for test
RUN mkdir -p /app/bin
COPY ./docker/entrypoint.sh /app/bin/
COPY ./requirements.txt /app/
COPY ./tests /app/tests
COPY ./config /app/config
COPY ./data /app/data

COPY docker/nginx/nginx.conf /etc/nginx/
COPY docker/nginx/default /etc/nginx/sites-available/


RUN pip install -r requirements.txt -i ${PIP_REPO}

RUN apt-get clean && rm -fr /tmp/* && rm -rf /var/lib/apt/lists/* && rm -rf /root/.cache/pip

CMD ["bash", "bin/entrypoint.sh"]
