# main.py

import sys
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from main_layout import MainLayout


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainLayout()

    # setup stylesheet
    apply_stylesheet(app=app, theme='dark_teal.xml')

    sys.exit(app.exec_())

