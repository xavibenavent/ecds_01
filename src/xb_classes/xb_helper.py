# xb_helper.py

import hashlib

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def hash256(s) -> bytes:
    '''two rounds of sha256'''
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def encode_base58(s) -> str:
    count = 0
    for c in s:  # <1>
        if c == 0:
            count += 1
        else:
            break
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:  # <2>
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result  # <3>


def encode_base58_checksum(b) -> str:
    return encode_base58(b + hash256(b)[:4])
