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

from PyQt5.QtCore import QObject, QFile, QIODevice, QTextStream
import re


class SubtitleParse(QObject):
    def __init__(self, subtitle, encoding="UTF-8"):
        super().__init__()

        subtitlefile = QFile(subtitle)

        if not subtitlefile.open(QIODevice.ReadOnly | QIODevice.Text):
            return

        text = QTextStream(subtitlefile)
        text.setCodec(encoding)

        subtitletext = text.readAll()

        # ('sıra', 'saat', 'dakika', 'saniye', 'milisaniye', 'saat', 'dakika', 'saniye', 'milisaniye', 'birincisatır', 'ikincisatır')
        compile = re.compile(r"(\d.*)\n(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})\n(\W.*|\w.*)\n(\w*|\W*|\w.*|\W.*)\n")
        self.sublist = compile.findall(subtitletext)


    def parse(self):
        liste = []

        for sub in self.sublist:
            saat = int(sub[1]) * 60 * 60 * 1000
            dk = int(sub[2]) * 60 * 1000
            sn = int(sub[3]) * 1000
            ms = int(sub[4]) + saat + dk + sn

            lsaat = int(sub[5]) * 60 * 60 * 1000
            ldk = int(sub[6]) * 60 * 1000
            lsn = int(sub[7]) * 1000
            lms = int(sub[8]) + lsaat + ldk + lsn

            if sub[10] != "":
                liste.append((ms, lms, "{}\n{}".format(sub[9], sub[10])))
            else:
                liste.append((ms, lms, sub[9]))

        return liste



if __name__ == "__main__":
    asd = SubtitleParse("/media/metehan/Depo/The Martian.srt")
    print(asd.parse())