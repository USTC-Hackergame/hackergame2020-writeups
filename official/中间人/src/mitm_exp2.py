from pwn import *
from hashlib import sha256

# context.log_level = 'debug'

r = remote('127.0.0.1', 10041)

r.recvuntil('token: ')
r.sendline('这里填写你的 token')

r.recvuntil('? ')
r.sendline('2')

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

def pad(msg):
    n = 16 - len(msg) % 16
    return msg + bytes([n]) * n

def xor(b1, b2):
    return bytes([x ^ y for x, y in zip(b1, b2)])

def crc128(msg):
    crc = (1 << 128) - 1
    for b in msg:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ (0xB595CF9C8D708E2166D545CF7CFDD4F9 & -(crc & 1))
    return (crc ^ ((1 << 128) - 1)).to_bytes(16, "big")

def construct(offset, tail, target):
    length = (offset + tail) * 8 + 128
    crc = ((int.from_bytes(target, 'big') ^ ((1 << 128) - 1)) << length) ^ ((1 << 128) - 1)
    for _ in range(length):
        crc = (crc >> 1) ^ (0xB595CF9C8D708E2166D545CF7CFDD4F9 & -(crc & 1))
    length = tail * 8 + 128
    crc <<= length
    for i in range(length):
        if crc & (1 << (128 + length - i - 1)):
            crc ^= (0xB595CF9C8D708E2166D545CF7CFDD4F9 * 2 + 1) << (length - 1 - i)
    msg = crc.to_bytes(16, "little")
    return b'\x00' * offset + msg + b'\x00' * tail

l = len(enc(b'', b''))
payload = b''
while len(enc(b'', payload)) == l:
    payload += b'a'
flaglen = l + 16 - 16 - 16 - 16 - 7 - 21 - len(payload)
print(flaglen)

flag = b''
for i in range(flaglen):
    namelen = 16 - (7 + 21 + flaglen - len(flag)) % 16 + 1 + 16
    prefixlen = 7 + namelen + 21 + flaglen - len(flag) - 1
    assert prefixlen % 16 == 0
    ct = enc(namelen * b'a', b'a' * 16)
    blk = ct[prefixlen + 16: prefixlen + 16 + 16]
    for c in range(256):
        blk_p = (bytes([c]) + flag + b'a' * 15)[:16]
        blk_iv = ct[prefixlen: prefixlen + 16]
        change = xor(xor(xor(b"Thanks aaaaaaaaa", blk_p), ct[:16]), blk_iv) + xor(blk, ct[16:32])
        new_iv = xor(ct[:16], construct(0, 16, crc128(change)))
        payload = new_iv + blk + ct[32:]
        if check(payload):
            flag = bytes([c]) + flag
            print(flag)
            break
    else:
        print('not found')
        exit(-1)
