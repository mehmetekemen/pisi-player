from PyQt5.QtWidgets import QToolBox, QPushButton, QColorDialog, QFontComboBox, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import QPoint, Qt, pyqtSignal
from .settings import settings

class SubtitleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        hlayout = QHBoxLayout()
        self.setLayout(hlayout)

        font_combobox = QFontComboBox()
        font_combobox.setEditable(False)
        font_combobox.setFixedHeight(30)
        font_combobox.setStyleSheet("QFontComboBox {background-color: white; color: black; border-radius: 3px;\
                                     border-color: lightgray; border-style: solid; border-width:2px;} \
                                     QFontComboBox::down-arrow {image: url(/usr/share/icons/breeze/actions/24/arrow-down)} \
                                     QFontComboBox::drop-down {border:none;}")
        font_combobox.setCurrentText(settings().value("Subtitle/font"))
        hlayout.addWidget(font_combobox)

        self.color_button = QPushButton()
        self.color_button.setFixedSize(30, 30)
        self.color_button.setStyleSheet("QPushButton {border: 1px solid black; border-radius: 3px; \
                                    background-color: %s; }"%(settings().value("Subtitle/color") or QColor("#ffffff")).name())
        hlayout.addWidget(self.color_button)

        self.color_button.clicked.connect(self.colorSelected)
        font_combobox.currentIndexChanged[str].connect(self.fontChanged)

    def fontChanged(self, font):
        settings().setValue("Subtitle/font", font)
        settings().sync()
        self.parent.settingsChanged.emit()

    def colorSelected(self):
        color = QColorDialog.getColor(Qt.white, self)
        if not color.name() == "#000000":
            settings().setValue("Subtitle/color", color)
            settings().sync()
            self.color_button.setStyleSheet("QPushButton {border: 1px solid black; border-radius: 3px; \
                                        background-color: %s; }"%color.name())
            self.parent.settingsChanged.emit()

class YoutubeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent


class FalancaWidget(QWidget): pass

class SettingsDialog(QToolBox):

    settingsChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowFlags(Qt.Tool)
        self.setVisible(False)
        self.resize(300, 250)
        self.move(settings().value("Settings/position") or QPoint(250,250))
        self.setWindowIcon(QIcon.fromTheme("pisiplayer"))
        self.setWindowTitle(self.tr("Ayarlar"))
        self.setStyleSheet("""QToolBox::tab {
                            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                        stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                                        stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
                            border-radius: 5px;
                            color: darkgray;
                            }

                            QToolBox::tab:selected { /* italicize selected tabs */
                                font: italic;
                                color: white;
                            }""")

        page1 = self.addItem(SubtitleWidget(self), self.tr("Altyazılar"))

        page2 = self.addItem(YoutubeWidget(self), self.tr("Youtube"))

    def closeEvent(self, event):
        settings().setValue("Settings/position", self.pos())
        settings().sync()
        event.accept()

