from PyQt5.QtWidgets import qApp
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaMetaData
from PyQt5.QtGui import QIcon, QPainter, QBrush, QFont, QPen, QColor
from PyQt5.QtCore import QUrl, Qt, QEvent, QRect
import sys


class Player(QVideoWidget):
    def __init__(self, parent=None):
        super().__init__()
        #self.resize(640, 450)
        self.parent = parent

        self.setMouseTracking(True)

        self.player = QMediaPlayer()
        content = QMediaContent(QUrl.fromLocalFile(sys.argv[1]))
        self.player.setMedia(content)
        self.player.play()

        self.player.setVideoOutput(self)

    def sliderChanged(self, pos):
        self.player.setPosition(pos)

    def mousePressEvent(self, event):
        print(event.type())
        event.accept()


    def mouseDoubleClickEvent(self, event):
        if not self.parent.isFullScreen():
            self.parent.showFullScreen()
        else:
            self.parent.showNormal()
        event.accept()


    def play(self):
        self.player.play()

    def stop(self):
        self.player.stop()

    def pause(self):
        self.player.pause()

    def setMuted(self, mute):
        self.player.setMuted(mute)

    def mutedState(self):
        if self.player.isMuted():
            self.setMuted(False)
        else:
            self.setMuted(True)

    def isMuted(self):
        return  self.player.isMuted()

    def setVolume(self, value):
        self.player.setVolume(value)

    def volume(self):
        return self.player.volume()