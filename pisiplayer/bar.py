from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QSpacerItem, QSizePolicy, QAbstractSlider
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import time
from .baritems.slider import PlayerSlider

class Bar(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.setFixedHeight(55)

        self.parent = parent

        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlayout)

        self.video_slider = PlayerSlider(self)
        self.video_slider.triggerAction(QAbstractSlider.SliderMove)
        self.video_slider.setOrientation(Qt.Horizontal)
        self.vlayout.addWidget(self.video_slider)

        self.hlayout = QHBoxLayout()
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.vlayout.addLayout(self.hlayout)

        self.hlayout.addItem(QSpacerItem(10, 10, QSizePolicy.Preferred, QSizePolicy.Minimum))

        self.play_and_pause_button = QPushButton(self)
        self.play_and_pause_button.setFlat(True)
        self.play_and_pause_button.setFixedSize(32, 32)
        self.play_and_pause_button.setIcon(QIcon(":/data/images/pause.svg"))
        self.play_and_pause_button.setIconSize(QSize(32, 32))
        self.hlayout.addWidget(self.play_and_pause_button)

        self.sound_button = QPushButton(self)
        self.sound_button.setFlat(True)
        self.sound_button.setFixedSize(32, 32)
        self.sound_button.setIcon(QIcon(":/data/images/volume3.svg"))
        self.sound_button.setIconSize(QSize(32, 32))

        self.sound_volume_slider = QSlider(self)
        self.sound_volume_slider.setFixedWidth(100)
        self.sound_volume_slider.setMinimum(0)
        self.sound_volume_slider.setMaximum(100)
        self.sound_volume_slider.setValue(100)
        self.sound_volume_slider.setOrientation(Qt.Horizontal)

        self.hlayout.addWidget(self.sound_button)
        self.hlayout.addWidget(self.sound_volume_slider)

        self.video_time = QLabel(self)
        self.video_time.total_time = 0
        self.video_time.current_time = 0
        self.video_time.setStyleSheet("color: rgb(255, 255, 255);")
        self.video_time.setText("00:00/00:00")
        self.hlayout.addWidget(self.video_time)

        self.hlayout.addItem(QSpacerItem(100, 10, QSizePolicy.Preferred, QSizePolicy.Minimum))

        self.cc_button = QPushButton(self)
        self.cc_button.setFlat(True)
        self.cc_button.setIcon(QIcon(":data/images/altyazi.svg"))
        self.cc_button.setIconSize(QSize(32, 32))
        self.cc_button.setFixedSize(32, 32)

        self.hlayout.addWidget(self.cc_button)

        self.fullscreen_button = QPushButton(self)
        self.fullscreen_button.setFlat(True)
        self.fullscreen_button.setIcon(QIcon(":data/images/fullscreen.svg"))
        self.fullscreen_button.setIconSize(QSize(32, 32))
        self.fullscreen_button.setFixedSize(32, 32)

        self.hlayout.addWidget(self.fullscreen_button)

        self.hlayout.addItem(QSpacerItem(10, 10, QSizePolicy.Preferred, QSizePolicy.Minimum))

        self.sound_volume_slider.valueChanged.connect(self.volumeSlider)

        self.fullscreen_button.clicked.connect(self.fullScreenState)



    def fullScreenState(self):
        if self.parent.isFullScreen():
            self.parent.showNormal()
        else:
            self.parent.showFullScreen()


    def videoSliderMax(self, mvalue):
        self.video_slider.setMaximum(mvalue)
        self.video_time.total_time = mvalue

    def timeToString(self, ctime, ttime):
        if (ttime/1000) >= 360:
            return time.strftime("%H:%M:%S", time.gmtime(ctime / 1000)), time.strftime("%H:%M:%S", time.gmtime(ttime / 1000))
        else:
            return time.strftime("%M:%S", time.gmtime(ctime / 1000)), time.strftime("%M:%S", time.gmtime(ttime / 1000))

    def videoSliderValue(self, value):
        self.video_slider.setValue(value)
        self.video_time.current_time = value
        self.video_time.setText("%s/%s"%(self.timeToString(self.video_time.current_time, self.video_time.total_time)))


    def volumeSlider(self, volume):
        self.sound_volume_slider.setValue(volume)
        if not self.sound_volume_slider.value():
            self.sound_button.setIcon(QIcon(":/data/images/volumeX.svg"))
        elif self.sound_volume_slider.value() < 15 and self.sound_volume_slider.value() > 0:
            self.sound_button.setIcon(QIcon(":/data/images/volume.svg"))
        elif self.sound_volume_slider.value() < 40 and self.sound_volume_slider.value() >= 15:
            self.sound_button.setIcon(QIcon(":/data/images/volume1.svg"))
        elif self.sound_volume_slider.value() < 70 and self.sound_volume_slider.value() >= 40:
            self.sound_button.setIcon(QIcon(":/data/images/volume2.svg"))
        elif self.sound_volume_slider.value() <= 100 and self.sound_volume_slider.value() >= 70:
            self.sound_button.setIcon(QIcon(":/data/images/volume3.svg"))

    def playingState(self, state):
        if state == 1:
            self.play_and_pause_button.setIcon(QIcon(":/data/images/pause.svg"))
        else:
            self.play_and_pause_button.setIcon(QIcon(":/data/images/play.svg"))

    def mutedChange(self, bool):
        if bool:
            self.sound_button.setIcon(QIcon(":/data/images/volumeX.svg"))
        else:
            self.volumeSlider(self.sound_volume_slider.value())