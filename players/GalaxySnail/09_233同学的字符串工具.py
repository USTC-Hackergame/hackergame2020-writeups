
for i in range(0x10ffff):
    c = chr(i)
    if c.upper() in "FLAG":
        print(f"{i=}, {c=}, {c.upper()=}")
ans1 = "ﬂag"

# https://zh.wikipedia.org/wiki/UTF-7
# g:  0    0    6    7
#  0b0000_0000_0110_0111
#  0b000000_000110_0111 00
#     0       6       28
#     A       G       c
# g -> +AGc-
ans2 = "fla+AGc-"
