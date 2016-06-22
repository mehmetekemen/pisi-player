from PyQt5.QtWidgets import QDialog, QListWidget, QListWidgetItem

class SettingsDialog(QListWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setVisible(False)
        self.resize(90, 100)
        self.setStyleSheet("QListWidget {background-color: rgba(22, 22, 22, 150); border-color:  rgba(22, 22, 22, 150);"\
                           "border-width: 1px; border-style outset; border-radius: 10px; color:white; font-weight:bold;}")

        a = QListWidgetItem(self)
        a.setText("Altyazılar")

        a = QListWidgetItem(self)
        a.setText("Youtube")

        a = QListWidgetItem(self)
        a.setText("Falanca")
