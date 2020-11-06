from pwn import *
import time
from tqdm import tqdm

threshold = 24

while True:
    re = remote('127.0.0.1', 10031)

    re.recvuntil("token: ")
    re.sendline('这里填写你的 token')

    re.recvuntil("n = ")
    n = int(re.recvline())
    re.recvuntil("e = ")
    e = int(re.recvline())
    re.recvuntil("x0 = ")
    x0 = int(re.recvline())
    re.recvuntil("x1 = ")
    x1 = int(re.recvline())

    cs = "0123456789abcdef"
    bits = 1024
    scale = 19

    table = [[] for _ in range(256)]
    for i in cs:
        for j in cs:
            v = ord(i) + scale * ord(j)
            table[v % 256].append((i, j, v // 256))

    v = (x0 + pow(scale, e, n) * x1) * pow(1 + pow(scale, e, n), -1, n) % n

    re.recvuntil("v = ")
    re.sendline(str(v))

    re.recvuntil("m0_ = ")
    m0_ = int(re.recvline())
    re.recvuntil("m1_ = ")
    m1_ = int(re.recvline())

    start_r = (m0_ + m1_ * scale) % n
    while True:
        cands = {start_r: ([], 1)}
        for b in range(bits // 8):
            ncands = {}
            for r, (m0, cnt) in cands.items():
                for i, j, carry in table[r % 256]:
                    new_r = r // 256 - carry
                    if new_r < 0:
                        continue
                    if new_r not in ncands:
                        ncands[new_r] = [], 0
                    l, old_cnt = ncands[new_r]
                    l.append((i, m0))
                    ncands[new_r] = l, old_cnt + cnt
            cands = ncands
            if not cands:
                break
        if cands:
            total = sum(cnt for _, (_, cnt) in cands.items())
            print(total, total.bit_length())
            break
        start_r += n
    if total < 2 ** threshold:
        break
    else:
        print("Too long")
        re.close()
        time.sleep(5)

def generate(l):
    for c, suffix in l:
        if suffix:
            for s in generate(suffix):
                yield c + s
        else:
            yield c

pbar = tqdm(total=total, position=0, leave=True)

target = (v - x0) % n

for _, (root, _) in cands.items():
    for m0 in generate(root):
        m0 = int.from_bytes(m0.encode(), 'big')
        if pow(m0_ - m0, e, n) == target:
            m1 = (start_r - m0) // scale
            m1t = m1.to_bytes(bits // 8, 'big')
            re.recvuntil("m0 = ")
            re.sendline(str(m0))
            re.recvuntil("m1 = ")
            re.sendline(str(m1))
            re.interactive()
            exit()
        pbar.update(1)
pbar.close()
