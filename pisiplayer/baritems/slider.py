from PyQt5.QtWidgets import QSlider, QStyle

class PlayerSlider(QSlider):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setFixedHeight(5)
        self.setStyleSheet("""QSlider::groove:horizontal {
    border: 1px solid red;
    height: 6px;
    margin: 2px 0;
border-radius: 3px;
}
QSlider::handle:horizontal {
    background: red;
    border: 1px solid red;
    width: 3px;
    margin: -8px 0;
    border-radius: 1px;
}
QSlider::add-page:horizontal {
    background: lightgray;
}
QSlider::sub-page:horizontal {
    background: red;
}""")


    def mousePressEvent(self, event):
        self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width()))
        self.sliderMoved.emit((event.x() / self.width()) * self.maximum())


    def mouseMoveEvent(self, event):
        self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width()))
        self.sliderMoved.emit((event.x() / self.width()) * self.maximum())


class SoundSlider(PlayerSlider):
    pass