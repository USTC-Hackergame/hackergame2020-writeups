from Crypto.Cipher import AES


def pad(msg):
    n = AES.block_size - len(msg) % AES.block_size
    return msg + bytes([n]) * n


def unpad(msg):
    assert len(msg) > 0 and len(msg) % AES.block_size == 0
    n = msg[-1]
    assert 1 <= n <= AES.block_size
    assert msg[-n:] == bytes([n]) * n
    return msg[:-n]


def xor(b1, b2):
    return bytes([x ^ y for x, y in zip(b1, b2)])


def crc128(msg):
    crc = (1 << 128) - 1
    for b in msg:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ (0xB595CF9C8D708E2166D545CF7CFDD4F9 & -(crc & 1))
    return (crc ^ ((1 << 128) - 1)).to_bytes(16, "big")


def hmac_crc128(key, msg):  # RFC 2104
    opad = b"\x5c" * 16
    ipad = b"\x36" * 16
    return crc128(xor(key, opad) + crc128(xor(key, ipad) + msg))
