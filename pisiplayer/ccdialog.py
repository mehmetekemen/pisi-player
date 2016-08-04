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

from PyQt5.QtWidgets import QDialog, QComboBox, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal
from .settings import settings

class CCDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setVisible(False)
        self.setStyleSheet("QDialog {background-color: rgba(22, 22, 22, 150); border-color:  rgba(22, 22, 22, 150);" \
                           "border-width: 1px; border-style outset; border-radius: 10px; color:white; font-weight:bold;}")

        layout = QHBoxLayout()
        self.setLayout(layout)

        label = QLabel()
        label.setStyleSheet("QLabel {color:white;}")
        label.setText("Kodlama:")

        layout.addWidget(label)

        self.combobox = QComboBox()
        self.combobox.addItems(["ISO 8859-9", "UTF-8"])
        self.combobox.setStyleSheet("QComboBox {background-color: rgba(22, 22, 22, 150); border-color:  rgba(22, 22, 22, 150);" \
                           " color:white; font-weight:bold;}")
        self.combobox.setCurrentText(settings().value("Subtitle/codec"))

        layout.addWidget(self.combobox)

        self.combobox.currentTextChanged.connect(self.textCodecChange)


    subtitleCodecChanged = pyqtSignal(str)
    def textCodecChange(self, codec):
        self.subtitleCodecChanged.emit(codec)
        settings().setValue("Subtitle/codec", self.combobox.currentText())
        settings().sync()