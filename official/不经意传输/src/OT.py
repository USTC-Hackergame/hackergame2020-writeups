from Crypto.PublicKey import RSA
from random import SystemRandom
import os


if __name__ == "__main__":
    random = SystemRandom()

    key = RSA.generate(1024)
    print("n =", key.n)
    print("e =", key.e)

    m0 = int.from_bytes(os.urandom(64).hex().encode(), "big")
    m1 = int.from_bytes(os.urandom(64).hex().encode(), "big")

    x0 = random.randrange(key.n)
    x1 = random.randrange(key.n)
    print("x0 =", x0)
    print("x1 =", x1)

    v = int(input("v = "))
    m0_ = (m0 + pow(v - x0, key.d, key.n)) % key.n
    m1_ = (m1 + pow(v - x1, key.d, key.n)) % key.n
    print("m0_ =", m0_)
    print("m1_ =", m1_)

    guess0 = int(input("m0 = "))
    guess1 = int(input("m1 = "))
    if guess0 == m0:
        print(open("flag1").read())
        if guess1 == m1:
            print(open("flag2").read())
    else:
        print("Nope")
