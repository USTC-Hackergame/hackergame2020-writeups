FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install Flask-Session pillow numpy matplotlib pyopenssl
COPY ./app /app