import os
os.environ['PWNLIB_NOTERM'] = "true"
from pwn import remote
from sage.all import *

# context.log_level = 'debug'

r = remote('127.0.0.1', 10041)

r.recvuntil('token: ')
r.sendline('这里填写你的 token')

r.recvuntil('? ')
r.sendline('3')

def enc(name, extra):
    r.recvuntil('? ')
    r.sendline('Alice')
    r.recvuntil('? ')
    r.sendline(name.hex())
    r.recvuntil('? ')
    r.sendline(extra.hex())
    r.recvuntil(':\n')
    return bytes.fromhex(r.recvline().decode().strip())

def check(cipher):
    r.recvuntil('? ')
    r.sendline('Bob')
    r.recvuntil(': ')
    r.sendline(cipher.hex())
    reply = r.recvline()
    return  b'Thanks' in reply

assert check(enc(b'abc', b'def'))

# 16 IV
# 7 text
# ? name
# 21 text
# flag
# ? extra
# 16 crc128
# 16 padding

def xor(b1, b2):
    return bytes([x ^ y for x, y in zip(b1, b2)])

def crc128(msg):
    crc = (1 << 128) - 1
    for b in msg:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ (0xB595CF9C8D708E2166D545CF7CFDD4F9 & -(crc & 1))
    return (crc ^ ((1 << 128) - 1)).to_bytes(16, "big")

l = len(enc(b'', b''))
payload = b''
while len(enc(b'', payload)) == l:
    payload += b'a'
flaglen = l + 16 - 16 - 16 - 16 - 7 - 21 - len(payload)
print(flaglen)

N = 150

flag = b''
while len(flag) < flaglen:
    namelen = 16 - (7 + 21 + flaglen - len(flag)) % 16 + 1 + 16 + 16 * N
    prefixlen = 7 + namelen + 21 + flaglen - len(flag) - 1
    assert prefixlen % 16 == 0
    ct = enc(namelen * b'a', b'a' * 32)
    blk_flagprev_c = ct[prefixlen: prefixlen + 16]
    blk_flag_c = ct[prefixlen + 16: prefixlen + 16 + 16]
    blk_flagnext_c = ct[prefixlen + 32: prefixlen + 16 + 32]
    blk_flagnext_p = (b'_' + flag + b'a' * 32)[16:32]
    changes = []
    strs = []
    for i in range(N):
        blk0_c = ct[16 * i + 16: 16 * i + 16 + 16]
        blk1_c = ct[16 * i + 32: 16 * i + 16 + 32]
        blk1_p = b'a' * 16
        change = xor(xor(xor(blk0_c, blk1_p), blk_flag_c), blk_flagnext_p) + xor(blk1_c, blk_flagnext_c)
        strs.append(b'\x00' * 16 * (i + 1) + change + b'\x00' * 16 * (N - 1 - i))
        changes.append(crc128(strs[-1]))
    A = Matrix(GF(2), 128, N)
    for i in range(128):
        for j in range(N):
            A[i, j] = (int.from_bytes(changes[j], 'big') >> i) & 1
    for c in range(256):
        blk_flag_p = (bytes([c]) + flag + b'a' * 32)[:16]
        target = xor(xor(xor(b"Thanks aaaaaaaaa", ct[:16]), blk_flagprev_c), blk_flag_p) + xor(ct[16:32], blk_flag_c)
        target_str = target + b'\x00' * 16 * N
        target = crc128(target_str)

        B = vector(GF(2), 128)
        for i in range(128):
            B[i] = (int.from_bytes(target, 'big') >> i) & 1
        result = A.solve_right(B)

        # x = b'\x00' * 16 * (N + 1)
        # for i in range(N):
        #     if result[i]:
        #         x = xor(x, strs[i])
        # assert crc128(x) == target

        payload = ct[:16] + blk_flag_c + b''.join(blk_flagnext_c if result[i] else ct[16 * i + 32: 16 * i + 16 + 32] for i in range(N)) + ct[16+16+16*N:]
        if check(payload):
            flag = bytes([c]) + flag
            print(flag)
            break
