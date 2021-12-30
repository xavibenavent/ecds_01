# xb_public_key.py


from src.xb_classes.xb_private_key import XBPrivateKey


class XBPublicKey:
    def __init__(self, private_key: XBPrivateKey):
        self.private_key = private_key
