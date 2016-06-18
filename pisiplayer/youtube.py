from urllib.request import urlopen, urlparse
from urllib.parse import parse_qs


class Youtube(object):
    def __init__(self, url):

        _videourl = urlparse(url)
        _videoid = _videourl.query[2:]

        self._get_video_info =  parse_qs(urlopen("https://www.youtube.com/get_video_info?video_id={}".format(_videoid)).read().decode("utf-8"))
        self._stream_map = self._get_video_info["url_encoded_fmt_stream_map"][0].split(",")

    def video_list(self):
        videos = []
        for i in self._stream_map:
            video = {}
            video["url"] = parse_qs(i)["url"][0]
            video["quality"] = parse_qs(i)["quality"][0]
            video["type"] = parse_qs(i)["type"][0].split(";")[0]
            videos.append(video)

        return videos


    def video_id(self):
        return self._get_video_info["video_id"][0]

    def video_title(self):
        return self._get_video_info["title"][0]

    def video_author(self):
        return self._get_video_info["author"][0]

    def has_video_cc(self):
        return self._get_video_info["has_cc"][0]


if __name__ == "__main__":
    you = Youtube("https://www.youtube.com/watch?v=gvVHSndpkEg")
    print(you.video_id(), you.video_title(), you.video_author(), you.has_video_cc(), you.video_list())
    you = Youtube("https://www.youtube.com/watch?v=NkceiLLNtao")
    print(you.video_id(), you.video_title(), you.video_author(), you.has_video_cc(), you.video_list())