FROM python:3.8
RUN python3 -m pip install -U pycryptodome
COPY entry.py MITM1.py MITM2.py MITM3.py utils.py /
CMD ["/usr/local/bin/python3", "-u", "/entry.py"]
