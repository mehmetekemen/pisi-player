from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import time
from .baritems.slider import PlayerSlider, SoundSlider
from .settings import settings


class Bar(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setFixedHeight(40)
        self.setStyleSheet("QWidget {background-color: transparent;} QPushButton:flat { border: none; }")
        self.parent = parent
        self.setFocusPolicy(Qt.NoFocus)


        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlayout)

        self.video_slider = PlayerSlider(self)
        self.video_slider.setOrientation(Qt.Horizontal)
        self.vlayout.addWidget(self.video_slider)
        self.video_slider.setFocusPolicy(Qt.NoFocus)

        self.hlayout = QHBoxLayout()
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.vlayout.addLayout(self.hlayout)

        self.hlayout.addItem(QSpacerItem(10, 10, QSizePolicy.Preferred, QSizePolicy.Minimum))

        self.play_and_pause_button = QPushButton(self)
        self.play_and_pause_button.setFocusPolicy(Qt.NoFocus)
        self.play_and_pause_button.setFlat(True)
        self.play_and_pause_button.setFixedSize(24, 24)
        self.play_and_pause_button.setIcon(QIcon(":/data/images/pause.png"))
        self.play_and_pause_button.setIconSize(QSize(24, 24))
        self.hlayout.addWidget(self.play_and_pause_button)

        self.sound_button = QPushButton(self)
        self.sound_button.setFocusPolicy(Qt.NoFocus)
        self.sound_button.setFlat(True)
        self.sound_button.setFixedSize(24, 24)
        self.sound_button.setIcon(QIcon(":/data/images/volume3.svg"))
        self.sound_button.setIconSize(QSize(24, 24))

        self.sound_volume_slider = SoundSlider(self)
        self.sound_volume_slider.setFocusPolicy(Qt.NoFocus)
        self.sound_volume_slider.setFixedWidth(80)
        self.sound_volume_slider.setMinimum(0)
        self.sound_volume_slider.setMaximum(100)
        self.sound_volume_slider.setValue(self.parent.player.volume())
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
        self.cc_button.setFocusPolicy(Qt.NoFocus)
        self.cc_button.setFlat(True)
        self.cc_button.setIcon(QIcon(":data/images/subtitle.png"))
        self.cc_button.setVisible(False)
        self.cc_button.setIconSize(QSize(24, 24))
        self.cc_button.setFixedSize(24, 24)

        self.hlayout.addWidget(self.cc_button)

        self.youtube_button = QPushButton(self)
        self.youtube_button.setFocusPolicy(Qt.NoFocus)
        self.youtube_button.setFlat(True)
        self.youtube_button.setIcon(QIcon(":data/images/youtube.png"))
        self.youtube_button.setIconSize(QSize(24, 24))
        self.youtube_button.setFixedSize(24, 24)

        self.hlayout.addWidget(self.youtube_button)

        self.settings_button = QPushButton(self)
        self.settings_button.setFocusPolicy(Qt.NoFocus)
        self.settings_button.setFlat(True)
        self.settings_button.setIcon(QIcon(":data/images/settings.svg"))
        self.settings_button.setIconSize(QSize(24, 24))
        self.settings_button.setFixedSize(24, 24)

        self.hlayout.addWidget(self.settings_button)

        self.fullscreen_button = QPushButton(self)
        self.fullscreen_button.setFocusPolicy(Qt.NoFocus)
        self.fullscreen_button.setFlat(True)
        self.fullscreen_button.setIcon(QIcon(":data/images/fullscreen.png"))
        self.fullscreen_button.setIconSize(QSize(24, 24))
        self.fullscreen_button.setFixedSize(24, 24)

        self.hlayout.addWidget(self.fullscreen_button)

        self.hlayout.addItem(QSpacerItem(10, 10, QSizePolicy.Preferred, QSizePolicy.Minimum))

        self.sound_volume_slider.valueChanged.connect(self.volumeSlider)
        self.fullscreen_button.clicked.connect(self.fullScreenState)

        self.youtube_button.clicked.connect(self.parent.youtubeDialog)
        self.settings_button.clicked.connect(self.parent.settingsDialog)


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

        settings().setValue("Player/volume", volume)
        settings().sync()

    def playingState(self, state):
        if state == 1:
            self.play_and_pause_button.setIcon(QIcon(":/data/images/pause.png"))
        else:
            self.play_and_pause_button.setIcon(QIcon(":/data/images/play.png"))

    def mutedChange(self, bool):
        if bool:
            self.sound_button.setIcon(QIcon(":/data/images/volumeX.svg"))
        else:
            self.volumeSlider(self.sound_volume_slider.value())