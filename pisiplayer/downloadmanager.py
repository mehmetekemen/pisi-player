from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl


class DownloadManager(QNetworkAccessManager):
    def __init__(self, parent=None):
        super().__init__(parent)


    def addUrl(self, url):
        print(url)
        self.request = QNetworkRequest(QUrl(url))
        self.request.setRawHeader(b"User-Agent", b"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1")

        self.reply = self.get(self.request)

        self.reply.downloadProgress.connect(self.setProgress)

        return self.request

    def setProgress(self, a, s):
        print(a, s)
