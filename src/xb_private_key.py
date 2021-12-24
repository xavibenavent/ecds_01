# xb_private_key.py


from secrets import token_hex
from hashlib import sha256

PRIVATE_KEY_BYTES_LENGTH = 32


class XBPrivateKey:
    """
    :param key_hex private key in HEX
    """
    def __init__(self, key_hex: str):
        # check param validity
        if not isinstance(key_hex, str) or len(key_hex) != PRIVATE_KEY_BYTES_LENGTH * 2:  # each byte 2 hex digits
            raise Exception('Private key not valid')

        # private key value in HEX
        self.key = key_hex

        # todo: private key compressed WIF format
        self.cwif = None

    """
    constructor-like method to create a random private key
    """
    @classmethod
    def from_random(cls):
        key_hex = token_hex(32)
        return cls(key_hex=key_hex)

    """
    constructor-like method to create a private key from a 32 bytes HEX string
    :param key_hex private key in HEX
    """
    @classmethod
    def from_hex(cls, key_hex: str):
        return cls(key_hex=key_hex)

    """
    constructor-like method to create a private key from a passphrase
    :param passphrase
    """
    @classmethod
    def from_passphrase(cls, passphrase: str):
        key_hex = cls._passphrase_to_hex(passphrase)
        return cls(key_hex)

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

    def wif(self, compressed=True, testnet=False):
        secret_bytes = self.key.to_bytes(32, 'big')
        if testnet:
            prefix = b'\xef'
        else:
            prefix = b'\x80'
        if compressed:
            suffix = b'\x01'
        else:
            suffix = b''
        return encode_base58_checksum(prefix + secret_bytes + suffix)


if __name__ == '__main__':
    a = XBPrivateKey.from_random()
    print(a.key)

    b = XBPrivateKey.from_hex(a.key)
    print(b.key)

    c = XBPrivateKey.from_passphrase('')
    print(c.key)