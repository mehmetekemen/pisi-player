from PyQt5.QtWidgets import QGraphicsTextItem
from .subtitleparse import SubtitleParse
from PyQt5.QtCore import QTimer, QFile

class SubtitleItemText(QGraphicsTextItem):

    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.timer = QTimer(self)

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
        self.setHtml("")
        self.timer.timeout.disconnect()

    def positionValue(self, pos):
        if self.subtitle_list:
            for ctime, ltime, subtitle in self.subtitle_list:
                if abs(pos - ctime) <= 200:
                    self.timer.timeout.connect(self.clearHtml)
                    self.setHtml("<h1 style='color: white;'>%s</h1>"%subtitle)
                    self.setPos((self.parent.size().width() - self.document().size().width()) / 2, self.parent.size().height() - 150)
                    self.timer.start(ltime-ctime)
                    break

"""
pos değeri 100ms de bir döner.
ctime ile arasında +-100ms varsa ekrana basılır.
ltime-ctime süre kadar durur ve silinir.
"""