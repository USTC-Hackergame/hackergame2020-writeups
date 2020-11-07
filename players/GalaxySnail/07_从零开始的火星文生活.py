import operator as op
from functools import reduce

FILENAME = "gibberish_message.txt"

with open(FILENAME, "r", encoding="utf-8") as f:
    for i, s in enumerate(f):
        if i == 2:
            print(f"{s=}")
            s = s.strip()[1::2]
            print(f"{s=}")
            break

def chr2int(c: str) -> int:
    x, y = c.encode("gbk")
    return (x << 8) | y

s_arr = list(map(chr2int, s))

and_ = reduce(op.and_, s_arr)
or_  = reduce(op.or_,  s_arr)
print(bin(and_))
print(bin(or_))
print(bin(and_ ^ or_))
# 0b0000001_00111111

def dec(c: int) -> int:
    return ((c & 0b1_00000000) >> 2) | (c & 0b111111)

b = bytes(map(dec, s_arr))
print(f"{b=}")

