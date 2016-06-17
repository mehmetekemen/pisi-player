from urllib.request import urlopen, urlparse
from urllib.parse import parse_qs


class Youtube(object):
    def __init__(self, url):

        _videourl = urlparse(url)
        _videoid = _videourl.query[2:]

        self._get_video_info =  parse_qs(urlopen("https://www.youtube.com/get_video_info?video_id={}".format(_videoid)).read())
        self._stream_map = self._get_video_info[b"url_encoded_fmt_stream_map"][0].split(b",")

    def video_list(self):
        videos = []
        for i in self._stream_map:
            video = {}
            video["url"] = parse_qs(i)[b"url"][0]
            video["quality"] = parse_qs(i)[b"quality"][0]
            video["type"] = parse_qs(i)[b"type"][0].split(b";")[0]
            videos.append(video)

        return videos


    def video_id(self):
        return self._get_video_info[b"video_id"][0]

    def video_title(self):
        return self._get_video_info[b"title"][0]

    def video_author(self):
        return self._get_video_info[b"author"][0]

    def has_video_cc(self):
        return self._get_video_info[b"has_cc"][0]


if __name__ == "__main__":
    you = Youtube("https://www.youtube.com/watch?v=gvVHSndpkEg")
    print(you.video_id(), you.video_title(), you.video_author(), you.has_video_cc())
    for i in you.video_list():
        print(i)