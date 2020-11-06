#!/usr/bin/env python3

from Crypto.Cipher import AES
import os
from hashlib import sha256
from utils import *


def talk_to_Alice():
    name = bytes.fromhex(input("What's your name? "))
    extra = bytes.fromhex(input("What else do you want to say? "))
    msg = b"Thanks " + name + b" for taking my flag: " + flag + extra
    plaintext = msg + sha256(msg).digest()
    iv = os.urandom(AES.block_size)
    aes = AES.new(AES_key, AES.MODE_CBC, iv)
    print("This is my encrypted message, please take it to Bob:")
    print((iv + aes.encrypt(pad(plaintext))).hex())


def talk_to_Bob():
    try:
        ciphertext = bytes.fromhex(input("Show me your message from Alice: "))
        iv = ciphertext[: AES.block_size]
        aes = AES.new(AES_key, AES.MODE_CBC, iv)
        plaintext = unpad(aes.decrypt(ciphertext[AES.block_size :]))
        assert sha256(plaintext[:-32]).digest() == plaintext[-32:]
        print("Thanks")
    except:
        print("What's your problem???")


if __name__ == "__main__":
    flag = open("flag1").read().encode()
    AES_key = os.urandom(16)
    while True:
        choice = input("Whom do you want to talk to? ")
        if choice == "Alice":
            talk_to_Alice()
        elif choice == "Bob":
            talk_to_Bob()
