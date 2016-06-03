from PyQt5.QtWidgets import QApplication, qApp, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSizeF, QTimer
from .videoplayer import Player
from .bar import Bar
import sys
from pisiplayer import pisiplayer_rc


class PisiPlayer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__()
        self.resize(640, 480)
        self.setWindowTitle("Pisi Player")
        self.setWindowIcon(QIcon(":/data/images/pisiplayer.svg"))
        self.setStyleSheet("background-color: black; border: none;")
        self.setScene(QGraphicsScene())
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)




        self.player = Player(self)
        self.scene().addItem(self.player)
        self.player.playerPlayOrOpen(qApp.arguments())

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

        self.cursorTimer = QTimer(self)
        self.cursorTimer.timeout.connect(self.mouseAndBarHideOrShow)
        self.cursorTimer.start(3000)

    def mouseAndBarHideOrShow(self):
        self.bar.hide()

    def mouseMoveEvent(self, event):
        if event.pos():
            self.bar.show()
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

        if event.key() == Qt.Key_Up:
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


def main():

    app = QApplication(sys.argv)
    pisiplayer = PisiPlayer()
    pisiplayer.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()