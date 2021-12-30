# xb_private_key.py


from secrets import token_hex
from hashlib import sha256
import hmac
from src.xb_classes.xb_helper import encode_base58_checksum
from src.programming_bitcoin_classes.ecc import N, G, Signature

PRIVATE_KEY_BYTES_LENGTH = 32
# N = 0XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


class XBPrivateKey:
    """
    :param key_int private key as an int number
    """
    def __init__(self, key_int: int):
        # check param validity
        if key_int < 1 or key_int >= N:
            raise Exception('Private key not valid [out of range [1, N)')

        # private key value in HEX
        self.key_int = key_int

        self.relative_position = key_int / N * 100

        # private key in HEX
        self.key_hex = f'{self.key_int:x}'.zfill(64)

    """
    constructor-like method to create a random private key
    """
    @classmethod
    def from_random(cls):
        # generate random
        key_hex = token_hex(32)
        # convert to int
        key_int = int(key_hex, 16)
        return cls(key_int=key_int)

    """
    constructor-like method to create a private key from a 32 bytes HEX string
    :param key_hex private key in HEX
    """
    @classmethod
    def from_hex(cls, key_hex: str):
        # validate HEX string
        if len(key_hex) > PRIVATE_KEY_BYTES_LENGTH * 2:
            raise Exception('max length must be 64 char (32 bytes)')
        return cls(key_int=int(key_hex, 16))

    """
    constructor-like method to create a private key from a passphrase
    :param passphrase
    """
    @classmethod
    def from_passphrase(cls, passphrase: str):
        key_hex = cls._passphrase_to_hex(passphrase)
        return cls(key_int=int(key_hex, 16))

    """
    method to add custom complexity at the conversion process from passphrase to private key in HEX
    :param passphrase
    :return private key in HEX string
    """
    @staticmethod
    def _passphrase_to_hex(passphrase: str) -> str:
        # hash of the half first hash and half second hash combined
        first_hash = sha256(passphrase.encode()).hexdigest()
        second_hash = sha256(first_hash.encode()).hexdigest()
        combined = first_hash[:32] + second_hash[32:]
        third_hash = sha256(combined.encode()).hexdigest()
        return third_hash

    def get_wif(self, compressed=True, testnet=False) -> str:
        key_bytes = self.key_int.to_bytes(32, 'big')
        prefix = b'\xef' if testnet else b'\x80'
        suffix = b'\x01' if compressed else b''
        return encode_base58_checksum(prefix + key_bytes + suffix)

    def sign(self, z: int) -> Signature:  # z is hash256 of the thing being signed
        k = self.deterministic_k(z)
        # r is the x coordinate of the resulting point k*G
        r = (k * G).x.num
        # remember 1/k = pow(k, N-2, N)
        k_inv = pow(k, N - 2, N)
        # s = (z+r*secret) / k
        s = (z + r * self.key_int) * k_inv % N
        if s > N / 2:
            s = N - s
        # return an instance of Signature:
        # Signature(r, s)
        return Signature(r, s)

    def deterministic_k(self, z: int) -> int:
        k = b'\x00' * 32
        v = b'\x01' * 32
        if z > N:
            z -= N
        z_bytes = z.to_bytes(32, 'big')
        secret_bytes = self.key_int.to_bytes(32, 'big')
        s256 = sha256
        k = hmac.new(k, v + b'\x00' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b'\x01' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, 'big')
            if candidate >= 1 and candidate < N:
                return candidate
            k = hmac.new(k, v + b'\x00', s256).digest()
            v = hmac.new(k, v, s256).digest()


if __name__ == '__main__':
    a = XBPrivateKey.from_random()
    print(a.key_hex)
    print(a.relative_position)
    print(a.get_wif(compressed=True, testnet=False))

    b = XBPrivateKey.from_hex(a.key_hex)
    print(b.key_hex)

    c = XBPrivateKey.from_passphrase('aloha2')
    print(c.key_hex)
