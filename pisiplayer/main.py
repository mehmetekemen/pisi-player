from PyQt5.QtWidgets import QApplication, qApp, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSizeF, QTimer, QPointF, QSize, QPoint
from .videoplayer import Player
from .bar import Bar
from .subtitileitem import SubtitleItemText
from  .settings import settings
import sys, os
from pisiplayer import pisiplayer_rc


class PisiPlayer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__()
        self.resize((settings().value("Player/resize") or QSize(640, 480)))
        self.move((settings().value("Player/position") or QPoint(250, 150)))
        self.setWindowTitle("Pisi Player")
        self.setWindowIcon(QIcon(":/data/images/pisiplayer.svg"))
        self.setStyleSheet("background-color: black; border: none;")
        self.setScene(QGraphicsScene())
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAcceptDrops(True)

        self.subtitleitem = SubtitleItemText(self)
        self.player = Player(self)
        self.scene().addItem(self.player)


        self.scene().addItem(self.subtitleitem)


        self.bar = Bar(self)
        self.scene().addWidget(self.bar)

        self.player.player.durationChanged.connect(self.bar.videoSliderMax)
        self.player.player.positionChanged.connect(self.bar.videoSliderValue)

        self.player.player.mutedChanged.connect(self.bar.mutedChange)
        self.player.player.stateChanged.connect(self.bar.playingState)
        self.player.player.volumeChanged.connect(self.bar.volumeSlider)

        self.bar.play_and_pause_button.clicked.connect(self.playOrPause)
        self.bar.sound_button.clicked.connect(self.player.mutedState)
        self.bar.sound_volume_slider.valueChanged.connect(self.player.setVolume)

        self.bar.video_slider.sliderMoved.connect(self.player.sliderChanged)

        self.player.subtitlePos.connect(self.subtitleitem.positionValue)
        self.player.isSubtitle.connect(self.bar.cc_button.setVisible)

        self.cursorTimer = QTimer(self)
        self.cursorTimer.timeout.connect(self.mouseAndBarHideOrShow)
        self.cursorTimer.start(3000)

        self.player.playerPlayOrOpen(qApp.arguments())

    def mouseAndBarHideOrShow(self):
        self.bar.hide()
        self.setCursor(Qt.BlankCursor)

    def mouseMoveEvent(self, event):
        if event.pos():
            self.bar.show()
            self.setCursor(Qt.ArrowCursor)
            self.cursorTimer.start(3000)

    def playOrPause(self):
        if self.player.player.state() == self.player.player.PlayingState:
            self.player.pause()
        elif self.player.player.state() == self.player.player.StoppedState or self.player.player.PausedState:
            self.player.play()

    def mouseDoubleClickEvent(self, event):
        if not self.isFullScreen():
            self.showFullScreen()
        else:
            self.showNormal()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.isFullScreen():
            self.showNormal()

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close()
            sys.exit()

        if event.key() == Qt.Key_Space:
            if self.player.player.state() == self.player.player.PlayingState:
                self.player.pause()
            elif self.player.player.state() == self.player.player.StoppedState or self.player.player.PausedState:
                self.player.play()

        if event.key() == Qt.Key_Plus:
            self.player.setVolume(self.player.volume() + 5)

        if event.key() == Qt.Key_Minus:
            self.player.setVolume(self.player.volume() - 5)

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_M:
            self.player.setMuted(not self.player.isMuted())

        if event.key() == Qt.Key_Right:
            self.player.player.setPosition(self.player.player.position() + 10000)

        if event.key() == Qt.Key_Left:
            self.player.player.setPosition(self.player.player.position() - 10000)

        if event.key() == Qt.Key_Up:
            self.player.player.setPosition(self.player.player.position() + 60000)

        if event.key() == Qt.Key_Down:
            self.player.player.setPosition(self.player.player.position() - 60000)

        super().keyPressEvent(event)

    def wheelEvent(self, event):
        if event.angleDelta().y() < 0:
            self.player.player.setPosition(self.player.player.position() - 60000)
        else:
            self.player.player.setPosition(self.player.player.position() + 60000)

    def resizeEvent(self, event):
        self.scene().setSceneRect(0, 0, event.size().width(), event.size().height())
        self.player.setSize(QSizeF(event.size().width(), event.size().height()))
        self.bar.setGeometry(0, event.size().height()-self.bar.height(), event.size().width(), self.bar.height())
        self.subtitleitem.setPos(QPointF((event.size().width()-self.subtitleitem.document().size().width())/2, event.size().height() - 150))
        self.bar.tube_dialog.setGeometry((event.size().width()-self.bar.tube_dialog.width())/2,
                                         (event.size().height()-self.bar.tube_dialog.height())/2,
                                         self.bar.tube_dialog.width(), self.bar.tube_dialog.height())
        self.bar.settings_dialog.setGeometry(event.size().width() - self.bar.settings_dialog.width() - 30,
                                         event.size().height() - self.bar.settings_dialog.height() - (20 + self.bar.height()),
                                         self.bar.settings_dialog.width(), self.bar.settings_dialog.height())

    def dragEnterEvent(self, event):
        uzantilar = ["mp4", "mkv", "webm", "ogv", "ogg", "avi", "flv", "wmv", "mpg", "mov", "srt"]
        if len(event.mimeData().urls()) < 2:
            if event.mimeData().urls()[0].toLocalFile().split(".")[-1] in uzantilar:
                event.accept()


    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        if event.mimeData().urls()[0].toLocalFile().split(".")[-1] == "srt":
            self.subtitleitem.addSubtitle(event.mimeData().urls()[0].toLocalFile())
            self.player.timerStart()
        else:
            self.player.addVideo(event.mimeData().urls()[0].toLocalFile())
        event.accept()

    def closeEvent(self, event):
        video_name = os.path.basename(self.player.player.media().canonicalUrl().toLocalFile())
        videos = settings().value("Player/video_names") or []
        videos_time = settings().value("Player/videos_time") or []
        try:
            videos_time[videos.index(video_name)] = self.player.player.position()
        except ValueError:
            videos.append(video_name)
            videos_time.append(self.player.player.position())
        settings().setValue("Player/video_names", videos)
        settings().setValue("Player/videos_time", videos_time)
        settings().setValue("Player/position", self.pos())
        settings().setValue("Player/resize", self.size())
        settings().sync()
        event.accept()

def main():

    app = QApplication(sys.argv)
    app.setOrganizationName("Pisi Linux")
    app.setApplicationName("Pisi Player")
    app.setApplicationVersion("0.7")
    pisiplayer = PisiPlayer()
    pisiplayer.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()