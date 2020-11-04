FROM python:3.8
RUN python3 -m pip install -U sympy
COPY server.py /
CMD ["/usr/local/bin/python3", "-u", "/server.py"]
