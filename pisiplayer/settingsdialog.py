from PyQt5.QtWidgets import QDialog, QListWidget, QListWidgetItem

class SettingsDialog(QListWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.setGeometry(300,100,100, 250)

        a = QListWidgetItem(self)
        a.setText("Altyazılar")

        a = QListWidgetItem(self)
        a.setText("Youtube")

        a = QListWidgetItem(self)
        a.setText("Falanca")
