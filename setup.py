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

from setuptools import setup, find_packages
from os import listdir, system


"""langs = []
for l in listdir('languages'):
    if l.endswith('ts'):
        system('lrelease-qt5 languages/%s' % l)
        langs.append(('languages/%s' % l).replace('.ts', '.qm'))"""


system('pyrcc5 pisiplayer.qrc -o pisiplayer/pisiplayer_rc.py')

datas = [('/usr/share/applications', ['data/pisiplayer.desktop']),
         ('/usr/share/icons/hicolor/256x256/apps', ['data/images/pisiplayer.svg']),
         #('/usr/share/kaptan/languages', langs)
         ]

setup(
    name = "pisiplayer",
    scripts = ["script/pisiplayer"],
    packages = find_packages(),
    version = "0.9",
    license = "GPL v3",
    description = "Video Player for Pisi Linux",
    author = "Metehan Özbek",
    author_email = "mthnzbk@gmail.com",
    url = "https://github.com/mthnzbk/pisi-player",
    keywords = ["PyQt5"],
    data_files = datas
)

