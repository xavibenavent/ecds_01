# secp256k1_tab.py

from PyQt5.QtWidgets import QTabWidget, QFormLayout, QLineEdit
from src.programming_bitcoin_classes.ecc import G, P, N

P_STR = '2 ** 256 - 2 ** 32 - 977'


class Secp256k1(QTabWidget):
    def __init__(self):
        super().__init__()

        form_layout = QFormLayout()

        # to align the layout in Mac OSX (this is the windows default)
        form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        # Secp256k1 parameters
        self.gx = QLineEdit(str(G.x))
        self.gy = QLineEdit(str(G.y))
        self.p_def = QLineEdit(P_STR)
        self.p_dec = QLineEdit(str(P))
        self.p_hex = QLineEdit(str(hex(P)).upper()[2:])
        # self.p_bin = QTextEdit(str(bin(P))[2:])
        # self.p_bin.setFixedHeight(50)
        self.n = QLineEdit(str(hex(N))[2:])

        form_layout.addRow('Secp256k1', None)
        form_layout.addRow('G (x)', self.gx)
        form_layout.addRow('G (y)', self.gy)
        form_layout.addRow('P (def)', self.p_def)
        form_layout.addRow('P (dec)', self.p_dec)
        form_layout.addRow('P (hex)', self.p_hex)
        # form_layout.addRow('P (bin)', self.p_bin)
        form_layout.addRow('N (hex)', self.n)
        point = N * G
        form_layout.addRow('N * G', QLineEdit(str(point)))

        self.setLayout(form_layout)
