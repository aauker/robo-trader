FROM python:3.10.2-buster

RUN apt-get update && apt-get install -y build-essential python-dev tini

# spams install error with 1.22.x
RUN pip --no-cache-dir install --upgrade pip && \
    pip --no-cache-dir install numpy==1.22.0 

RUN pip --no-cache-dir install boto3 datetime websocket-client[optional] configparser

COPY . /robo-trader

ENV ROOT_CFG_DIR=/
ENV AWS_CONFIG_FILE=/.aws/config
ENV AWS_SHARED_CREDENTIALS_FILE=/.aws/credentials

WORKDIR /robo-trader
CMD ["tini", "--", "python3", "-m", "stream-alpaca-news.stream"]