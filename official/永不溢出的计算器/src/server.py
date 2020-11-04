from sympy import sqrt_mod, nextprime
from sympy.ntheory.modular import crt
import random
import os
import hashlib
import math

flag = int.from_bytes(open("flag", "rb").read(), "big")
token = os.environ["hackergame_token"]
secret = "43c5cf58ed8872cbbfb9625f0dcaf6e0"

p = int.from_bytes(hashlib.sha512((secret + "1" + token).encode()).digest(), "big")
q = int.from_bytes(hashlib.sha512((secret + "2" + token).encode()).digest(), "big")
while True:
    p = nextprime(p)
    q = nextprime(q)
    n = p * q
    if math.gcd(65537, (p - 1) * (q - 1)) == 1:
        break

print("This is a calculator mod n")
print("You can try: a + b, a - b, a * b, a / b, a ^ b, sqrt(a)")
print("Be aware of the spaces around operators")
print("flag ^ 65537 =", pow(flag, 65537, n))

while True:
    line = input("> ")
    line = line.strip()
    try:
        if line.startswith("sqrt(") and line.endswith(")"):
            a = int(line[5:-1]) % n
            a1l = sqrt_mod(a, p, True)
            a2l = sqrt_mod(a, q, True)
            ans = []
            for a1 in a1l:
                for a2 in a2l:
                    r = int(crt([p, q], [a1, a2])[0]) % n
                    assert pow(r, 2, n) == a
                    ans.append(r)
            if ans:
                print(min(ans))
            else:
                print("Math error")
        else:
            a, op, b = line.split()
            a = int(a)
            b = int(b)
            if op == "+":
                print((a + b) % n)
            elif op == "-":
                print((a - b) % n)
            elif op == "*":
                print((a * b) % n)
            elif op == "/":
                try:
                    print((a * pow(b, -1, n)) % n)
                except ValueError:
                    print("Math error")
            elif op == "^":
                try:
                    print(pow(a, b, n))
                except ValueError:
                    print("Math error")
            else:
                print("Invalid input")
    except ValueError:
        print("Invalid input")
