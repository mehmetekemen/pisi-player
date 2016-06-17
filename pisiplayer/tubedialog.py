from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QHBoxLayout, QLabel, QVBoxLayout
from .youtube import *

class TubeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setGeometry(100, 25, 500, 100)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 130);")

        vlayout = QVBoxLayout()
        self.setLayout(vlayout)

        hlayout = QHBoxLayout()
        vlayout.addLayout(hlayout)


        self.tube_line = QLineEdit(self)
        self.tube_line.setStyleSheet("background-color: rgba(0, 0, 0, 0);\ncolor: rgb(255, 255, 255);")
        self.tube_line.setPlaceholderText("https://www.youtube.com/watch?v=mY--4-vzY6E")
        hlayout.addWidget(self.tube_line)

        self.tube_button = QPushButton(self)
        self.tube_button.setStyleSheet("background-color: rgba(0, 0, 0, 50);\ncolor: rgb(255, 255, 255);")
        self.tube_button.setText("Video Çek")
        hlayout.addWidget(self.tube_button)

        self.tube_warning = QLabel(self)
        self.tube_warning.setStyleSheet("color: rgb(255, 255, 255); font-weight: bold; background-color: rgba(0, 0, 0, 0);")
        self.tube_warning.setText("Verilen bağlantı geçersiz!")
        vlayout.addWidget(self.tube_warning)

        self.tube_line.returnPressed.connect(self.tube_button.animateClick)
        self.tube_button.clicked.connect(self.videoParse)

    def videoParse(self):
        self.close()

