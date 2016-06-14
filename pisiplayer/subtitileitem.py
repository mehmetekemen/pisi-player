from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtGui import QFont, QColor
from .subtitleparse import SubtitleParse
from PyQt5.QtCore import QTimer, QFile
import re

class SubtitleItemText(QGraphicsTextItem):

    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.timer = QTimer(self)
        self.font = QFont("Noto Serif", 20)
        self.setDefaultTextColor(QColor("white"))
        self.setFont(self.font)


    def paint(self, painter, op, w):
        painter.setBrush(QColor(0, 0, 0, 130))
        painter.drawRect(self.boundingRect())
        super().paint(painter, op, w)

    def addSubtitle(self, subtitle):
        self.subtitle_list = SubtitleParse(subtitle).parse()

    def subtitleControl(self, content):
        srt = content.canonicalUrl().toLocalFile().split(".")
        srt.pop(-1)
        srt.append("srt")
        srt = ".".join(srt)
        if QFile.exists(srt):
            self.subtitle_list = SubtitleParse(srt).parse()
        else:
            self.subtitle_list = None

    def clearHtml(self):
        self.setPlainText("")
        self.timer.timeout.disconnect()


    compile = re.compile(r"<(\w{1})><(\w{1})>(\w.+)<\/\w{1}><\/\w{1}>", re.S)
    def positionValue(self, pos):
        if self.subtitle_list:
            for ctime, ltime, subtitle in self.subtitle_list:
                if abs(pos - ctime) <= 200:
                    self.timer.timeout.connect(self.clearHtml)
                    sub = self.compile.search(subtitle)
                    print(subtitle)
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
                    self.timer.start(ltime-ctime)
                    break

"""
pos değeri 100ms de bir döner.
ctime ile arasında +-100ms varsa ekrana basılır.
ltime-ctime süre kadar durur ve silinir.
"""