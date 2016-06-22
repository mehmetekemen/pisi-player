from PyQt5.QtWidgets import QDialog, QComboBox, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal
from .settings import settings

class CCDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setVisible(False)
        self.setStyleSheet("QDialog {background-color: rgba(22, 22, 22, 150); border-color:  rgba(22, 22, 22, 150);" \
                           "border-width: 1px; border-style outset; border-radius: 10px; color:white; font-weight:bold;}")

        layout = QHBoxLayout()
        self.setLayout(layout)

        label = QLabel()
        label.setStyleSheet("QLabel {color:white;}")
        label.setText("Kodlama:")

        layout.addWidget(label)

        self.combobox = QComboBox()
        self.combobox.addItems(["ISO 8859-9", "UTF-8"])
        self.combobox.setCurrentText(settings().value("Subtitle/codec"))

        layout.addWidget(self.combobox)

        self.combobox.currentTextChanged.connect(self.textCodecChange)


    subtitleCodecChanged = pyqtSignal(str)
    def textCodecChange(self, codec):
        self.subtitleCodecChanged.emit(codec)
        settings().setValue("Subtitle/codec", self.combobox.currentText())
        settings().sync()