#
#
#  Copyright 2016 Metehan Özbek <mthnzbk@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QHBoxLayout, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPoint
from .youtube import Youtube
from .settings import settings

class TubeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.resize(400, 75)
        self.setWindowFlags(Qt.Tool)
        self.move(settings().value("Youtube/position") or QPoint(250, 250))
        self.setWindowIcon(QIcon.fromTheme("pisiplayer"))
        self.setWindowTitle(self.tr("Youtube'dan Oynat"))
        self.setStyleSheet("QDialog {background-color: rgba(255, 255, 255, 200); border-color:  rgba(255, 255, 255, 200); border-width: 1px; border-style outset;}")
        self.setVisible(False)

        vlayout = QVBoxLayout()
        self.setLayout(vlayout)

        hlayout = QHBoxLayout()
        vlayout.addLayout(hlayout)


        self.tube_line = QLineEdit(self)
        self.tube_line.setMinimumHeight(30)
        self.tube_line.setStyleSheet("QLineEdit {background-color: white; color: black; border-radius: 3px;\
                                     border-color: lightgray; border-style: solid; border-width:2px;}")
        self.tube_line.setPlaceholderText("https://www.youtube.com/watch?v=mY--4-vzY6E")
        hlayout.addWidget(self.tube_line)

        self.tube_button = QPushButton(self)
        self.tube_button.setMinimumHeight(30)
        self.tube_button.setStyleSheet("QPushButton {background-color: #55aaff; color: white; border-width:1px; font-weight: bold; \
                                       border-color: #55aaff; border-style: solid; padding-left: 3px; padding-right: 3px; border-radius: 3px;}")
        self.tube_button.setText(self.tr("Video Oynat"))
        hlayout.addWidget(self.tube_button)

        self.tube_warning = QLabel(self)
        self.tube_warning.setVisible(False)
        self.tube_warning.setStyleSheet("QLabel {color: rgb(255, 0, 0); font-weight: bold; background-color: white;}")
        self.tube_warning.setText(self.tr("Verilen bağlantı geçersiz!"))
        vlayout.addWidget(self.tube_warning)

        self.tube_line.returnPressed.connect(self.tube_button.animateClick)
        self.tube_button.clicked.connect(self.videoParse)

    def videoParse(self):
        self.tube_warning.setVisible(False)

        try:
            youtube = Youtube(self.tube_line.text())
            #youtube.video_title()
            self.parent.player.addYoutubeVideo(youtube.get_video(settings().value("Youtube/quality") or "medium",
                                                                 settings().value("Youtube/format") or "mp4"))
            self.close()

            # Başlık ------------ En kaliteli video url

        except:
            self.tube_warning.setVisible(True)

    def closeEvent(self, event):
        settings().setValue("Youtube/position", self.pos())
        settings().sync()
        event.accept()