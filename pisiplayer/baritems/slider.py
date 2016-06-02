from PyQt5.QtWidgets import QSlider, QStyle



class PlayerSlider(QSlider):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent


    def mousePressEvent(self, event):
        self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width()))
        self.sliderMoved.emit((event.x() / self.width()) * self.maximum())


    def mouseMoveEvent(self, event):
        self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width()))
        self.sliderMoved.emit((event.x() / self.width()) * self.maximum())