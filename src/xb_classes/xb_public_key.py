# xb_public_key.py

from src.xb_classes.xb_private_key import XBPrivateKey
from src.programming_bitcoin_classes.ecc import S256Point, N, G, Signature


class XBPublicKey:
    def __init__(self, private_key: XBPrivateKey):
        self.private_key = private_key

        # create public key point
        self.point: S256Point = private_key.key_int * G

    def __repr__(self):
        x_coord = f'{self.point.x}'.upper()
        y_coord = f'{self.point.y}'.upper()
        return 'x:' + x_coord + ' y:' + y_coord

    def get_sec_bin(self, compressed=True) -> bytes:
        '''returns the binary version of the SEC format'''
        if compressed:
            # 33 bytes length (1+32)
            # 66 chars length (33x2)
            if self.point.y.num % 2 == 0:
                return b'\x02' + self.point.x.num.to_bytes(32, 'big')
            else:
                return b'\x03' + self.point.x.num.to_bytes(32, 'big')
        else:
            # 65 bytes length (1+32+32)
            # 130 chars length (65x2)
            return b'\x04' + self.point.x.num.to_bytes(32, 'big') + \
                self.point.y.num.to_bytes(32, 'big')

    def get_sec_hex(self, compressed=True) -> str:
        # returns the hex version of the SEC format
        return self.get_sec_bin(compressed=compressed).hex().upper()

    def verify(self, z: int, sig: Signature) -> bool:
        # By Fermat's Little Theorem, 1/s = pow(s, N-2, N)
        s_inv = pow(sig.s, N - 2, N)
        # u = z / s
        u = z * s_inv % N
        # v = r / s
        v = sig.r * s_inv % N
        # u*G + v*P should have as the x coordinate, r
        total = u * G + v * self.point
        return total.x.num == sig.r


if __name__ == '__main__':
    priv_key = XBPrivateKey.from_random()
    pub_key = XBPublicKey(private_key=priv_key)
    print(f'private key (WIF): {pub_key.private_key.get_wif(compressed=True, testnet=False)}')
    print(f'public key point: {pub_key}')
    print(f'sec (compressed): {pub_key.get_sec_hex()}')
    print(f'sec (uncompressed): {pub_key.get_sec_hex(compressed=False)}')
    print(f'sec binary (compressed): {pub_key.get_sec_bin()}')



