from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl


class Player(QVideoWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setMouseTracking(True)

        self.player = QMediaPlayer()
        self.player.setVideoOutput(self)

    def playerPlayOrOpen(self, arg=None):
        if type(arg) == list and len(arg) > 1:
            content = QMediaContent(QUrl.fromLocalFile(arg[1]))
            self.player.setMedia(content)
            self.play()

    def addVideo(self, video):
        content = QMediaContent(QUrl.fromLocalFile(video))
        self.player.setMedia(content)
        self.play()

    def sliderChanged(self, pos):
        self.player.setPosition(pos)

    def mouseDoubleClickEvent(self, event):
        if not self.parent.isFullScreen():
            self.parent.showFullScreen()
        else:
            self.parent.showNormal()

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