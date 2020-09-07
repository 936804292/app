FROM python:3

RUN pip install -U pip

RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple

RUN pip config set install.trusted-host mirrors.aliyun.com

RUN pip freeze > requirements.txt

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN mkdir /app

copy . /app

WORKDIR /app

CMD ["sh","start.sh"]