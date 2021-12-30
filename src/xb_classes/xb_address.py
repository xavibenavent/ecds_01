# xb_address.py

from src.xb_classes.xb_private_key import XBPrivateKey
from src.xb_classes.xb_public_key import XBPublicKey
from src.xb_classes.xb_helper import encode_base58_checksum, hash160

from bech32 import encode as bech32_encode
from random import randint


class XBAddress:
    def __init__(self, public_key: XBPublicKey):
        self.public_key = public_key

    def get_base58(self, compressed: bool, testnet: bool) -> str:
        # get hash160
        sec: bytes = self.public_key.get_sec_bin(compressed=compressed)
        h160: bytes = hash160(bytes_to_hash=sec)
        if testnet:
            prefix = b'\x6f'
        else:
            prefix = b'\x00'
        return encode_base58_checksum(prefix + h160)

    def get_bech32(self, compressed: bool, testnet: bool) -> str:
        # get hash160
        sec: bytes = self.public_key.get_sec_bin(compressed=compressed)
        h160: bytes = hash160(bytes_to_hash=sec)
        if testnet:
            prefix = 'tb'
        else:  # mainnet
            prefix = 'bc'
        return bech32_encode(prefix, 0, h160)


if __name__ == '__main__':
    private_key = XBPrivateKey.from_hex(key_hex='7B56E2B7BD189F4491D43A1D209E6268046DF1741F61B6397349D7AA54978E76')
    public_key = XBPublicKey(private_key=private_key)
    address = XBAddress(public_key=public_key)
    print(f'base58: {address.get_base58(compressed=True, testnet=False)}')
    print(f'base58: {address.get_base58(compressed=True, testnet=True)}')
    print(f'bech32: {address.get_bech32(compressed=True, testnet=False)}')
    print(f'bech32: {address.get_bech32(compressed=True, testnet=True)}')

    # signature and verification
    z = randint(0, 2 ** 256)
    signature = address.public_key.private_key.sign(z)
    print(signature)
    print(address.public_key.verify(z, signature))

