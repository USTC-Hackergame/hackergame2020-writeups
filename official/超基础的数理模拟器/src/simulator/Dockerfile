FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./app /app

RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install requests pycryptodome pyopenssl