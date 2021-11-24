# ecds.py

from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QTextEdit, QVBoxLayout, QTabWidget
from src.secp256k1_tab import Secp256k1
from src.private_public_tab import PrivatePublicTab


class ECDSLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1200, 700)
        self.setWindowTitle('ECDS')

        layout = QVBoxLayout()
        tabs_widget = QTabWidget()

        sec256k1_tab = Secp256k1()
        private_public_tab = PrivatePublicTab()

        tabs_widget.addTab(sec256k1_tab, 'secp256k1')
        tabs_widget.addTab(private_public_tab, 'private/public')

        # add tabs to layout
        layout.addWidget(tabs_widget)

        # set main layout
        self.setLayout(layout)

        self.show()
