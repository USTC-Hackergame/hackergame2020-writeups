# 输出reversed(code)
print("reversed(code):")
# quotation = chr(0x22); s = "quotation = chr(0x22); s = {0}{1}{0}; s = {0}{0}.join(reversed(s.format(quotation, s))); print(s, end={0}{0})"; s = "".join(reversed(s.format(quotation, s))); print(s, end="")
quotation = chr(0x22)
s = "quotation = chr(0x22); s = {0}{1}{0}; s = {0}{0}.join(reversed(s.format(quotation, s))); print(s, end={0}{0})"
s = "".join(reversed(s.format(quotation, s)))
print(s, end="")

# 输出sha256(code)
print("\nsha256(code):")
# from hashlib import sha256; quotation = chr(0x22); s = "from hashlib import sha256; quotation = chr(0x22); s = {0}{1}{0}; s = s.format(quotation, s); h = sha256(s.encode({0}utf-8{0})).hexdigest(); print(h, end={0}{0})"; s = s.format(quotation, s); h = sha256(s.encode("utf-8")).hexdigest(); print(h, end="")
from hashlib import sha256
quotation = chr(0x22)
s = "from hashlib import sha256; quotation = chr(0x22); s = {0}{1}{0}; s = s.format(quotation, s); h = sha256(s.encode({0}utf-8{0})).hexdigest(); print(h, end={0}{0})"
s = s.format(quotation, s)
h = sha256(s.encode("utf-8")).hexdigest()
print(h, end="")