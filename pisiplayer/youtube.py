from urllib.request import urlopen, urlparse, urlsplit


class Youtube(object):
    def __init__(self, url):
        self._url = url