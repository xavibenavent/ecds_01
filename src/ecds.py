# ecds.py

from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QTextEdit, QVBoxLayout, QTabWidget
from src.secp256k1_tab import Secp256k1
from src.private_public_tab import PrivatePublicTab
from src.transaction_tab import TransactionTab


class ECDSLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(25, 25, 1400, 750)
        self.setWindowTitle('ECDS')

        layout = QVBoxLayout()
        tabs_widget = QTabWidget()

        sec256k1_tab = Secp256k1()
        private_public_tab = PrivatePublicTab()
        transaction_tab = TransactionTab()

        tabs_widget.addTab(sec256k1_tab, 'secp256k1')
        tabs_widget.addTab(private_public_tab, 'private/public')
        tabs_widget.addTab(transaction_tab,'transactions')

        # add tabs to layout
        layout.addWidget(tabs_widget)

        # set main layout
        self.setLayout(layout)

        self.show()
