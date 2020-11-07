import itertools
import csv
import re
from decimal import Decimal as D

FILENAME = "bills.csv"
PATTERN = re.compile(r"((\w+)元)?((\w+)角)?((\w+)分)?")

def str_to_num(s: str) -> int:
    if s is None:
        return 0
    chars = "壹贰叁肆伍陆柒捌玖"
    pattern = re.compile(r"(([{}])佰)?(([{}])?拾)?零?([{}])?".format(chars, chars, chars))
    match = pattern.match(s)
    val = 0
    if match.group(1):
        val += 100 * (chars.index(match.group(2)) + 1)
    if match.group(3):
        val += 10 * ((chars.index(match.group(4)) + 1) if match.group(4) else 1)
    if match.group(5):
        val += chars.index(match.group(5)) + 1
    # print(pattern.match(s).groups())
    return val


def moneystr_to_num(s: str):
    match = PATTERN.match(s)
    yuan, jiao, fen = map(str_to_num, map(match.group, (2, 4, 6)))
    return yuan + D("0.1")*jiao + D("0.01")*fen

def test(reader, n=20):
    for _, (money, amount) in itertools.takewhile(lambda x: x[0]<20, enumerate(reader)):
        if not _:
            continue
        print([money, amount])
        money_num = moneystr_to_num(money)
        assert type(money_num) is D
        print(money_num)

def main():
    with open(FILENAME, newline="", encoding="gbk") as f:
        reader = csv.reader(f)
        # test(reader)
        read_iter = iter(reader)
        next(read_iter)
        total = 0
        for money, amount in read_iter:
            money = moneystr_to_num(money)
            amount = int(amount)
            print(f"{money=}, {amount=}")
            total += money * amount
        print(total)

main()