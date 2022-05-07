#!/usr/bin/env python

import os.path
import sys
import urllib.request

from PySide6.QtWidgets import QApplication
from PySide6 import QtGui

from social_distance.core.processing import NETWORK_FILENAMES
from social_distance.widgets.main_window import MainWindow
import resources


def download_file(url, filename):
    if os.path.exists(filename):
        print("File already exists: {}".format(filename))
        return
    print("Downloading {} to {}".format(url, filename))
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, filename)


def download_large_files():
    nextcloud_folder = "https://nextcloud.pischulenok.xyz/s/iTpNXgwZbfEA4Ws/download?path=&files="
    files = [
        ('data', 'video', 'VID_20220506_123738_720p.mp4'),
        ('data', 'video', 'VID_20220506_123738_1080.mp4'),
        ('data', 'video', 'VID_20220506_124411_720.mp4'),
        ('data', 'video', 'VID_20220506_124411_1080.mp4'),
        *[('data', 'models', f'{fn}.weights') for fn in NETWORK_FILENAMES],
        *[('data', 'models', f'{fn}.cfg') for fn in NETWORK_FILENAMES],
    ]

    for path in files:
        try:
            os.makedirs(os.path.join(*path[:-1]))
        except FileExistsError:
            pass
        download_file(nextcloud_folder + path[-1], os.path.join(*path))


def main():
    # if getattr(sys, 'frozen', False):
    download_large_files()
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(':/icon.png'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
