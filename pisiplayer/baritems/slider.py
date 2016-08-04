#
#
#  Copyright 2016 Metehan Özbek <mthnzbk@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

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