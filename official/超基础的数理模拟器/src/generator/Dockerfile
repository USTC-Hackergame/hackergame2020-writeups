FROM sagemath/sagemath

RUN sudo sed -i 's/archive.ubuntu.com/mirrors.bfsu.edu.cn/g' /etc/apt/sources.list
RUN sage -pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN sage -pip install flask

ADD gen.sage /home/sage

EXPOSE 5000

ENTRYPOINT sage gen.sage