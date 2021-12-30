# xb_helper.py

from hashlib import sha256, new

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def hash256(bytes_to_hash: bytes) -> bytes:
    '''two rounds of sha256'''
    return sha256(sha256(bytes_to_hash).digest()).digest()


def hash160(bytes_to_hash: bytes) -> bytes:
    '''sha256 followed by ripemd160'''
    sha = sha256(bytes_to_hash).digest()
    return new('ripemd160', sha).digest()


def encode_base58(bytes_to_encode: bytes) -> str:
    count = 0
    for c in bytes_to_encode:  # <1>
        if c == 0:
            count += 1
        else:
            break
    num = int.from_bytes(bytes_to_encode, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:  # <2>
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result  # <3>


def encode_base58_checksum(bytes_to_encode: bytes) -> str:
    return encode_base58(bytes_to_encode + hash256(bytes_to_encode)[:4])
