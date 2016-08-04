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

from youtube_dl import YoutubeDL


class Youtube(object):
    def __init__(self, url):

        _youtube = YoutubeDL()
        self._videourl = _youtube.extract_info(url, download=False)


    def video_list(self):
        videos = []
        for item in self._videourl["formats"]:
            video = {}
            if item["format_note"] in ("medium", "hd720"):
                video["url"] = item["url"]
                video["ext"] = item["ext"]
                video["format"] = item["format_note"]
                #video[""] = item[""]
                videos.append(video)

        return videos

    def get_video_formats(self):
        formats = []
        for i in self.video_list():
            formats.append(i["format"])

        return formats

    def get_video_exts(self):
        exts = []
        for i in self.video_list():
            exts.append(i["ext"])

        return exts

    def get_video(self, quality="hd720", format="mp4"):
        if quality in self.get_video_formats():
            for i in self.video_list():
                if i["format"] == quality and i["ext"] == format:
                    return i["url"]
        else:
            for i in self.video_list():
                if i["format"] == "medium" and i["ext"] == format:
                    return i["url"]

    def video_id(self):
        return self._videourl["id"]

    def video_title(self):
        return self._videourl["title"]

    def video_author(self):
        return self._videourl["uploader_id"]

    def has_video_cc(self):
        return self._videourl["requested_subtitles"]

    def subtitles(self):
        return self._videourl["subtitles"]


if __name__ == "__main__":
    you = Youtube("https://www.youtube.com/watch?v=IEroLrjqFVc")
    print(you.video_id(), you.video_title(), you.video_author(), you.has_video_cc(), you.subtitles())
    for i in you.video_list():
        print(i)
    you = Youtube("https://www.youtube.com/watch?v=NkceiLLNtao")
    print(you.video_id(), you.video_title(), you.video_author(), you.has_video_cc(), you.subtitles())
    for i in you.video_list():
        print(i)