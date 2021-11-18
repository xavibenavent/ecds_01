# ecds.py

from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QTextEdit
from random import randint
from src.ecc import G, P, N, PrivateKey, S256Point

P_STR = '2 ** 256 - 2 ** 32 - 977'


class ECDSLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1200, 700)
        self.setWindowTitle('ECDS')

        form = QFormLayout()

        # to align the layout in Mac OSX (this is the windows default)
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        # Secp256k1 parameters
        self.gx = QLineEdit(str(G.x))
        self.gy = QLineEdit(str(G.y))
        self.p_def = QLineEdit(P_STR)
        self.p_dec = QLineEdit(str(P))
        self.p_hex = QLineEdit(str(hex(P)).upper()[2:])
        self.p_bin = QTextEdit(str(bin(P))[2:])
        self.p_bin.setFixedHeight(50)
        self.n = QLineEdit(str(hex(N))[2:])

        form.addRow('Secp256k1', None)
        form.addRow('G (x)', self.gx)
        form.addRow('G (y)', self.gy)
        form.addRow('P (def)', self.p_def)
        form.addRow('P (dec)', self.p_dec)
        form.addRow('P (hex)', self.p_hex)
        form.addRow('P (bin)', self.p_bin)
        form.addRow('N (hex)', self.n)
        point = N * G
        form.addRow('N * G', QLineEdit(str(point)))

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

        form.addRow('Private Key', None)
        form.addRow('secret', self.pkle)
        form.addRow('wif (compressed)', self.wif)
        form.addRow('wif (uncompressed)', self.wif_uncompressed)

        form.addRow('Public Key', None)
        form.addRow('pub_key (x)', self.pubkey_x)
        form.addRow('pub_key (y)', self.pubkey_y)
        form.addRow('sec (compressed)', self.sec)
        form.addRow('sec (uncompressed)', self.sec_uncompressed)
        form.addRow('address', self.address)

        self.setLayout(form)

        self.show()

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
