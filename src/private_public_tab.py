# private_public_tab.py

from PyQt5.QtWidgets import QTabWidget, QFormLayout, QLineEdit
from random import randint
from src.ecc import PrivateKey, S256Point

P_STR = '2 ** 256 - 2 ** 32 - 977'


class PrivatePublicTab(QTabWidget):
    def __init__(self):
        super().__init__()

        form_layout = QFormLayout()

        # to align the layout in Mac OSX (this is the windows default)
        form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        self.private_key = PrivateKey(secret=0)
        self.pkle = QLineEdit(str(self.private_key.secret))
        self.pkle.textChanged.connect(self.new_pk)
        self.pubkey_x = QLineEdit()
        self.pubkey_y = QLineEdit()

        self.wif = QLineEdit()
        self.wif_uncompressed = QLineEdit()
        self.sec = QLineEdit()
        self.sec_uncompressed = QLineEdit()
        self.address = QLineEdit()

        form_layout.addRow('Private Key', None)
        form_layout.addRow('secret', self.pkle)
        form_layout.addRow('wif (compressed)', self.wif)
        form_layout.addRow('wif (uncompressed)', self.wif_uncompressed)

        form_layout.addRow('Public Key', None)
        form_layout.addRow('pub_key (x)', self.pubkey_x)
        form_layout.addRow('pub_key (y)', self.pubkey_y)
        form_layout.addRow('sec (compressed)', self.sec)
        form_layout.addRow('sec (uncompressed)', self.sec_uncompressed)
        form_layout.addRow('address', self.address)

        self.setLayout(form_layout)

    def new_pk(self, text):
        if text == '' or text == '0':
            text = '1'
        self.private_key = PrivateKey(secret=int(text))
        self.pubkey_x.setText(str(self.private_key.point.x))
        self.pubkey_y.setText(str(self.private_key.point.y))
        print(self.private_key.wif())
        self.wif.setText(self.private_key.wif())
        self.wif_uncompressed.setText(self.private_key.wif(compressed=False))

        pub_key = S256Point(x=self.private_key.point.x, y=self.private_key.point.y)

        sec_compressed = pub_key.sec()
        sec_uncompressed = pub_key.sec(compressed=False)
        self.sec.setText(sec_compressed.hex())
        self.sec_uncompressed.setText(sec_uncompressed.hex())

        self.address.setText(pub_key.address())

        # signature
        z = randint(0, 2 ** 256)
        signature = self.private_key.sign(z)
        print(signature)
        print(pub_key.verify(z, signature))
