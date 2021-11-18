# main.py

import sys
from PyQt5.QtWidgets import QApplication

from ecds import ECDSLayout


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ECDSLayout()
    sys.exit(app.exec_())

