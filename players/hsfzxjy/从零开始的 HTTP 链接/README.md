# 从零开始的 HTTP 链接

此处提供一个使用 socket 编程完成 TCP 桥接的解法。

运行 `python3 bridge.py :8080 202.38.93.111:0`，浏览器访问 `localhost:8080` 即可。

```python
"""
python3 bridge.py :8080 202.38.93.111:0
"""

import sys
import socket
import select
import logging


def address(addr):
    host, port = addr.split(":", 1)
    return host, int(port)


def main(bind, connect, log_level):
    logging.basicConfig(level=log_level, format="%(asctime)s:%(levelname)s:%(message)s")
    serv = socket.create_server(bind)
    rtol = {}
    ltor = {}
    try:
        while True:
            readers, _, _ = select.select(
                tuple(rtol.values()) + tuple(ltor.values()) + (serv,), (), ()
            )
            for reader in readers:
                if reader is serv:
                    local_client, addr = reader.accept()
                    remote_client = socket.create_connection(connect)
                    ltor[local_client.fileno()] = remote_client
                    rtol[remote_client.fileno()] = local_client
                elif reader.fileno() in ltor:
                    data = reader.recv(2 ** 12)
                    if data:
                        logging.info("L -> R: %r", data)
                        ltor[reader.fileno()].sendall(data)
                    else:
                        remote = ltor[reader.fileno()]
                        del ltor[reader.fileno()], rtol[remote.fileno()]
                        remote.close()
                        reader.close()
                else:
                    data = reader.recv(2 ** 12)
                    if data:
                        logging.info("R -> L: %r", data)
                        rtol[reader.fileno()].sendall(data)
                    else:
                        local = rtol[reader.fileno()]
                        del rtol[reader.fileno()], ltor[local.fileno()]
                        reader.close()
                        local.close()
    except Exception as e:
        raise e
    finally:
        for sock in tuple(rtol.values()) + tuple(ltor.values()) + (serv,):
            sock.close()


if __name__ == "__main__":
    bind = address(sys.argv[1])
    connect = address(sys.argv[2])
    main(bind, connect, "INFO")
```