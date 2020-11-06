FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install pyopenssl XlsxWriter cn2an
RUN echo 'wsgi-disable-file-wrapper = true' >> /app/uwsgi.ini

COPY ./app /app
