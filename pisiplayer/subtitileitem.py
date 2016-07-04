from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtGui import QFont, QColor
from .subtitleparse import SubtitleParse
from PyQt5.QtCore import QFile
import re
from .settings import settings

class SubtitleItemText(QGraphicsTextItem):

    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent

        self.font = QFont(settings().value("Subtitle/font") or "Noto Serif", 20)
        self.setDefaultTextColor(settings().value("Subtitle/color") or QColor("white"))
        self.setFont(self.font)

    def settingsChanged(self):
        self.font = QFont(settings().value("Subtitle/font") or "Noto Serif", 20)
        self.setDefaultTextColor(settings().value("Subtitle/color") or QColor("white"))
        self.setFont(self.font)

    def paint(self, painter, op, wi):
        if self.toPlainText() != "":
            painter.setBrush(settings().value("Player/subtitle_background") or QColor(0, 0, 0, 130))
            painter.setPen(settings().value("Player/subtitle_background") or QColor(0, 0, 0, 130))
            x, y, w, h = self.boundingRect().x(), self.boundingRect().y()+5, self.boundingRect().width(), self.boundingRect().height()-5
            painter.drawRect(x, y, w, h)
        super().paint(painter, op, wi)

    def addSubtitle(self, subtitle):
        self.subtitle_file = subtitle
        self.subtitle_list = SubtitleParse(subtitle, settings().value("Subtitle/codec") or "ISO 8859-9").parse()

    def reParse(self, codec):
        self.subtitle_list = SubtitleParse(self.subtitle_file, codec).parse()

    def subtitleControl(self, content):
        srt = content.canonicalUrl().toLocalFile().split(".")
        srt.pop(-1)
        srt.append("srt")
        srt = ".".join(srt)
        if QFile.exists(srt):
            self.subtitle_file = srt
            self.subtitle_list = SubtitleParse(srt, settings().value("Subtitle/codec") or "ISO 8859-9").parse()
        else:
            self.subtitle_list = None


    compile = re.compile(r"<(\w{1})><(\w{1})>(\w.+)<\/\w{1}><\/\w{1}>", re.S)
    def subtitleItemParse(self, subtitle):
        sub = self.compile.search(subtitle)

        if sub:
            self.font.setItalic(True)
            self.font.setBold(True)
            self.setFont(self.font)
            self.setPlainText(sub.groups()[2])

        elif subtitle.startswith("<b>"):
            self.font.setBold(True)
            self.font.setItalic(False)
            self.setFont(self.font)
            self.setPlainText(subtitle[3:].split("<")[0])

        elif subtitle.startswith("<i>"):
            self.font.setItalic(True)
            self.font.setBold(False)
            self.setFont(self.font)
            self.setPlainText(subtitle[3:-4].split("<")[0])

        else:
            self.font.setBold(False)
            self.font.setItalic(False)
            self.setFont(self.font)
            self.setPlainText(subtitle)

        self.setPos((self.parent.size().width() - self.document().size().width()) / 2, self.parent.size().height() - 150)


    def positionValue(self, pos):
        if self.subtitle_list:
            for ctime, ltime, subtitle in self.subtitle_list:
                if pos - ctime >= 100 and ltime - pos >= 100:
                    self.subtitleItemParse(subtitle)
                    break

                else:
                    self.setPlainText("")
