FROM python:3.7

copy ../app/ /

WORKDIR /app

RUN pip install -U pip

RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple

RUN pip config set install.trusted-host mirrors.aliyun.com

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["sh","start.sh"]