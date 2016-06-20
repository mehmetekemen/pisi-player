from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QHBoxLayout, QLabel, QVBoxLayout
from .youtube import Youtube

class TubeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.resize(400, 75)
        self.setStyleSheet("QDialog {background-color: rgba(22, 22, 22, 150); border-color:  rgba(22, 22, 22, 150); border-width: 1px; border-style outset; border-radius: 10px;}")
        self.setVisible(False)

        vlayout = QVBoxLayout()
        self.setLayout(vlayout)

        hlayout = QHBoxLayout()
        vlayout.addLayout(hlayout)


        self.tube_line = QLineEdit(self)
        self.tube_line.setStyleSheet("QLineEdit {background-color: rgba(0, 0, 0, 0);\ncolor: rgb(255, 255, 255);}")
        self.tube_line.setPlaceholderText("https://www.youtube.com/watch?v=mY--4-vzY6E")
        hlayout.addWidget(self.tube_line)

        self.tube_button = QPushButton(self)
        self.tube_button.setStyleSheet("QPushButton {background-color: rgba(0, 0, 0, 50);\ncolor: rgb(255, 255, 255);}")
        self.tube_button.setText("Video Oynat")
        hlayout.addWidget(self.tube_button)

        self.tube_warning = QLabel(self)
        self.tube_warning.setVisible(False)
        self.tube_warning.setStyleSheet("QLabel {color: rgb(255, 255, 255); font-weight: bold; background-color: rgba(0, 0, 0, 0);}")
        self.tube_warning.setText("Verilen bağlantı geçersiz!")
        vlayout.addWidget(self.tube_warning)

        self.tube_line.returnPressed.connect(self.tube_button.animateClick)
        self.tube_button.clicked.connect(self.videoParse)

    def videoParse(self):
        self.tube_warning.setVisible(False)

        try:
            youtube = Youtube(self.tube_line.text())
            #youtube.video_title()
            self.parent.player.addYoutubeVideo(youtube.get_video())
            self.close()

            # Başlık ------------ En kaliteli video url

        except KeyError:
            self.tube_warning.setVisible(True)

