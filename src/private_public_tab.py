# private_public_tab.py

from PyQt5.QtWidgets import QTabWidget, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QCheckBox, QLabel
from random import randint
from src.ecc import PrivateKey, S256Point
from src.helper import xb_sha256

P_STR = '2 ** 256 - 2 ** 32 - 977'

TITLE_COLOR = 'LimeGreen'


class PrivatePublicTab(QTabWidget):
    def __init__(self):
        super().__init__()

        self.is_two_hash_rounds = False
        self.is_little_endian = False
        self.is_testnet = False

        form_layout = QFormLayout()

        # to align the layout in Mac OSX (this is the windows default)
        form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        self.setStyleSheet("QLineEdit {font-size: 12pt}")

        # controls
        controls = QHBoxLayout()

        # form_layout.addRow('Generate secret from sentence', None)
        generate_button = QPushButton('Generate secret')
        generate_button.pressed.connect(self.new_passphrase_button)

        # hash rounds check box
        hash_rounds = QCheckBox('Two hash rounds')
        hash_rounds.stateChanged.connect(self.hash_rounds_changed)

        # endianness check box
        endianness = QCheckBox('Little-endian (bytes to int)')
        endianness.stateChanged.connect(self.endianness_changed)

        # BTC network check box
        btc_network = QCheckBox('testnet (BTC Network Address)')
        btc_network.stateChanged.connect(self.btc_network_changed)

        controls.addWidget(generate_button)
        controls.addWidget(hash_rounds)
        controls.addWidget(endianness)
        controls.addWidget(btc_network)

        self.passphrase = QLineEdit()
        form_layout.addRow('Passphrase {str}', self.passphrase)
        form_layout.addRow('', controls)
        # form_layout.addRow('', generate_button)

        self.private_key = PrivateKey(secret=0)
        self.pkle = QLineEdit(str(self.private_key.secret))
        self.pkle_hex = QLineEdit(str(hex(self.private_key.secret)))
        self.pkle.textChanged.connect(self.new_pk)
        self.pubkey = QLineEdit()
        # self.pubkey_x = QLineEdit()
        # self.pubkey_y = QLineEdit()

        self.wif = QLineEdit()
        self.wif_uncompressed = QLineEdit()
        self.sec = QLineEdit()
        self.sec_uncompressed = QLineEdit()
        self.address = QLineEdit()
        self.address_uncompressed = QLineEdit()

        hash_title = QLabel('Hash algorithm')
        hash_title.setStyleSheet(f'color: {TITLE_COLOR}')
        form_layout.addRow(hash_title, None)

        self.sha256_x1 = QLineEdit()
        form_layout.addRow('SHA256 (x1) {hex} 64', self.sha256_x1)
        self.sha256_x2 = QLineEdit()
        form_layout.addRow('SHA256 (x2) {hex} 64', self.sha256_x2)

        private_key_title = QLabel('Private Key')
        private_key_title.setStyleSheet(f'color: {TITLE_COLOR}')
        form_layout.addRow(private_key_title, None)
        form_layout.addRow('secret {int}', self.pkle)
        # todo: force length to 64
        form_layout.addRow('secret {hex} 64', self.pkle_hex)
        form_layout.addRow('secret {base64} 44', QLineEdit('todo: encode base64'))
        form_layout.addRow('WIF COMPRESSED {base58} 52', self.wif)
        form_layout.addRow('WIF {base58} 51', self.wif_uncompressed)

        public_key_title = QLabel('Public Key')
        public_key_title.setStyleSheet(f'color: {TITLE_COLOR}')
        form_layout.addRow(public_key_title, None)
        form_layout.addRow('Point (X, Y) {hex} 64', self.pubkey)
        # form_layout.addRow('X {hex} 64', self.pubkey_x)
        # form_layout.addRow('Y {hex} 64', self.pubkey_y)
        form_layout.addRow('SEC COMPRESSED {hex} 66', self.sec)
        form_layout.addRow('SEC {hex} 130', self.sec_uncompressed)
        form_layout.addRow('BTC Address Compressed {base58}', self.address)
        form_layout.addRow('BTC Address {base58}', self.address_uncompressed)

        self.setLayout(form_layout)

    def new_passphrase_button(self):
        # encode passphrase to bytes
        passphrase = str.encode(self.passphrase.text())

        sha256x1_hex = xb_sha256(bytes_to_hash=passphrase, hex_return=True)
        self.sha256_x1.setText(sha256x1_hex.upper())

        # the input for the second hash has to be in bytes format
        sha256x1_dig = xb_sha256(bytes_to_hash=passphrase, hex_return=False)
        sha256x2_hex = xb_sha256(bytes_to_hash=sha256x1_dig, hex_return=True)
        sha256x2_dig = xb_sha256(bytes_to_hash=sha256x1_dig, hex_return=False)
        self.sha256_x2.setText(sha256x2_hex.upper())

        # hash256 + to little endian
        # self.private_key = little_endian_to_int(hash256(passphrase))

        # set endianness string
        endianness = 'little' if self.is_little_endian else 'big'

        # set number of hash rounds
        if not self.is_two_hash_rounds:
            self.private_key = int.from_bytes(sha256x1_dig, endianness)
        else:
            self.private_key = int.from_bytes(sha256x2_dig, endianness)

        self.pkle.setText(f'{self.private_key}')

    # output update when self.pkle text change
    def new_pk(self, text):
        if text == '' or text == '0':
            text = '1'
        self.private_key = PrivateKey(secret=int(text))
        self.pkle_hex.setText(hex(self.private_key.secret)[2:].upper())
        pubkey = f'({self.private_key.point.x} / {self.private_key.point.y})'
        self.pubkey.setText(pubkey.upper())
        # self.pubkey_x.setText(str(self.private_key.point.x).upper())
        # self.pubkey_y.setText(str(self.private_key.point.y).upper())
        self.wif.setText(self.private_key.wif())
        self.wif_uncompressed.setText(self.private_key.wif(compressed=False))

        pub_key = S256Point(x=self.private_key.point.x, y=self.private_key.point.y)

        sec_compressed = pub_key.sec()
        sec_uncompressed = pub_key.sec(compressed=False)
        self.sec.setText(sec_compressed.hex().upper())
        self.sec_uncompressed.setText(sec_uncompressed.hex().upper())

        self.address.setText(pub_key.address(compressed=True, testnet=self.is_testnet))
        self.address_uncompressed.setText(pub_key.address(compressed=False, testnet=self.is_testnet))

        # signature
        z = randint(0, 2 ** 256)
        signature = self.private_key.sign(z)
        print(signature)
        print(pub_key.verify(z, signature))

    def hash_rounds_changed(self, new_sate):
        self.is_two_hash_rounds = True if new_sate else False
        self.new_passphrase_button()

    def endianness_changed(self, new_state):
        self.is_little_endian = True if new_state else False
        self.new_passphrase_button()

    def btc_network_changed(self, new_sate):
        self.is_testnet = True if new_sate else False
        # since private key is not changed, is needed to force the call to new_pk()
        self.new_pk(self.pkle.text())
