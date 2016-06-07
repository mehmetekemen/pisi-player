from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import qApp


def settings():
    return  QSettings(qApp.organizationName(), qApp.applicationName())
