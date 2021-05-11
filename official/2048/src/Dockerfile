FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install pyopenssl

COPY ./app /app