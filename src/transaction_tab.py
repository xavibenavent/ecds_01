# transaction_tab.py

from typing import Any
from io import BytesIO
from PyQt5.QtWidgets import QTabWidget, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QTextEdit, QLabel
from src.helper import read_varint
from src.tx_input import TxInput



HEX_TX = '010000000456919960ac691763688d3d3bcea9ad6ecaf875df5339e\
148a1fc61c6ed7a069e010000006a47304402204585bcdef85e6b1c6af5c2669d4830ff86e42dd\
205c0e089bc2a821657e951c002201024a10366077f87d6bce1f7100ad8cfa8a064b39d4e8fe4e\
a13a7b71aa8180f012102f0da57e85eec2934a82a585ea337ce2f4998b50ae699dd79f5880e253\
dafafb7feffffffeb8f51f4038dc17e6313cf831d4f02281c2a468bde0fafd37f1bf882729e7fd\
3000000006a47304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1c\
dc26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071c1a716012\
1035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937feffffff567\
bf40595119d1bb8a3037c356efd56170b64cbcc160fb028fa10704b45d775000000006a4730440\
2204c7c7818424c7f7911da6cddc59655a70af1cb5eaf17c69dadbfc74ffa0b662f02207599e08\
bc8023693ad4e9527dc42c34210f7a7d1d1ddfc8492b654a11e7620a0012102158b46fbdff65d0\
172b7989aec8850aa0dae49abfb84c81ae6e5b251a58ace5cfeffffffd63a5e6c16e620f86f375\
925b21cabaf736c779f88fd04dcad51d26690f7f345010000006a47304402200633ea0d3314bea\
0d95b3cd8dadb2ef79ea8331ffe1e61f762c0f6daea0fabde022029f23b3e9c30f080446150b23\
852028751635dcee2be669c2a1686a4b5edf304012103ffd6f4a67e94aba353a00882e563ff272\
2eb4cff0ad6006e86ee20dfe7520d55feffffff0251430f00000000001976a914ab0c0b2e98b1a\
b6dbf67d4750b0a56244948a87988ac005a6202000000001976a9143c82d7df364eb6c75be8c80\
df2b3eda8db57397088ac46430600'

TITLE_COLOR = 'LimeGreen'


class TransactionTab(QTabWidget):
    def __init__(self):
        super().__init__()

        self.form_layout = QFormLayout()

        # to align the layout in Mac OSX (this is the windows default)
        self.form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        # form_layout.setFormAlignment(Qt.AlignTop)
        # form_layout.setVerticalSpacing(50)
        # form_layout.setAlignment(Qt.AlignTop)

        self.setStyleSheet("QLineEdit {font-size: 12pt}")

        # set controls line
        controls = QHBoxLayout()

        # form_layout.addRow('Generate secret from sentence', None)
        parse_button = QPushButton('Parse Tx')
        parse_button.pressed.connect(self.parse_tx_button)

        controls.addWidget(parse_button)

        self.tx = QTextEdit(HEX_TX)
        self.tx.setFixedHeight(200)
        self.form_layout.addRow('Tx to parse {str}', self.tx)
        self.form_layout.addRow('', controls)

        # version
        self.version = QLineEdit()
        self.form_layout.addRow('version', self.version)

        # inputs
        inputs = QLabel('Inputs')
        self.form_layout.addRow(inputs, None)
        self.inputs_count = QLineEdit()
        self.form_layout.addRow('inputs count', self.inputs_count)

        self.form_layout.addRow('Test row to delete when parsing', None)

        self.setLayout(self.form_layout)

    def parse_tx_button(self):
        # delete all rows but the first 5
        while self.form_layout.rowCount() > 5:
            last_row = self.form_layout.rowCount() -1
            self.form_layout.removeRow(last_row)

        # convert Tx in hex string format into a stream of bytes
        stream = BytesIO(bytes.fromhex(self.tx.toPlainText()))  # from a QTextEdit .toPlainText() has to be used

        version = self._parse_version(stream)
        self.version.setText(str(version))

        inputs_count = self._parse_inputs_count(stream)
        self.inputs_count.setText(str(inputs_count))

        # input transactions
        for tx_in in range(inputs_count):
            tx_input = self._parse_tx_input(stream)
            self.form_layout.addRow(f'#{tx_in}:', None)

    def _parse_version(self, stream: BytesIO) -> int:
        # get the first 4 bytes and convert to int with little endianness
        return int.from_bytes(stream.read(4), 'little')

    def _parse_inputs_count(self, stream: BytesIO) -> int:
        # it can read 1, 2, 4 or 8 bytes
        return read_varint(stream)

    def _parse_tx_input(self, stream: BytesIO) -> TxInput:
        pass
