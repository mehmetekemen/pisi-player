from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer, pyqtSignal, QFile
from .settings import settings
import os

class Player(QGraphicsVideoItem):

    subtitlePos = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.player = QMediaPlayer()
        self.player.setVolume(int(settings().value("Player/volume")) or 100)
        self.player.setVideoOutput(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timerPos)

        self.player.currentMediaChanged.connect(self.signalStart)
        self.player.currentMediaChanged.connect(self.parent.subtitleitem.subtitleControl)
        self.player.currentMediaChanged.connect(self.videoConfigure)

    def videoConfigure(self, media):
        video_name = os.path.basename(media.canonicalUrl().toLocalFile())
        videos = settings().value("Player/video_names") or []
        videos_time = settings().value("Player/videos_time") or []
        try:
            self.player.setPosition(int(videos_time[videos.index(video_name)]))
        except ValueError:
            pass

    def signalStart(self, content):
        srt = content.canonicalUrl().toLocalFile().split(".")
        srt.pop(-1)
        srt.append("srt")
        srt = ".".join(srt)
        if QFile.exists(srt):
            self.timer.start(200)
        else:
            self.timer.stop()

    def timerPos(self):
        self.subtitlePos.emit(self.player.position())

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