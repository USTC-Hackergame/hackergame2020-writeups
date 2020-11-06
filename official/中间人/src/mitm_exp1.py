from pwn import *
from hashlib import sha256

# context.log_level = 'debug'

r = remote('127.0.0.1', 10041)

r.recvuntil('token: ')
r.sendline('这里填写你的 token')

r.recvuntil('? ')
r.sendline('1')

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
# 32 sha256
# 16 padding

def pad(msg):
    n = 16 - len(msg) % 16
    return msg + bytes([n]) * n

l = len(enc(b'', b''))
payload = b''
while len(enc(b'', payload)) == l:
    payload += b'a'
flaglen = l + 16 - 16 - 32 - 16 - 7 - 21 - len(payload)
print(flaglen)

flag = b''
for i in range(flaglen):
    namelen = 16 - (7 + 21 + flaglen - len(flag)) % 16 + 1
    prefixlen = 7 + namelen + 21 + flaglen - len(flag) - 1
    assert prefixlen % 16 == 0
    for c in range(256):
        payload = pad(bytes([c]) + flag + sha256(bytes([c]) + flag).digest())[len(flag)+1:]
        ct = enc(namelen * b'a', payload)
        if check(ct[prefixlen:-32-16]):
            flag = bytes([c]) + flag
            print(flag)
            break
    else:
        print('not found')
        exit(-1)
