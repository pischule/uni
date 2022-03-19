import os.path
import sys

from PySide6.QtWidgets import QApplication

from gui.widgets.main_window import MainWindow
from util import download_file


def download_large_files():
    nextcloud_folder = "https://nextcloud.pischulenok.xyz/s/iTpNXgwZbfEA4Ws/download?path=&files="
    files = [
        ('video', 'vid0.mp4'),
        ('video', 'vid1.mp4'),
        ('video', 'vid2.avi'),
        ('models', 'yolov3.weights'),
        ('models', 'yolov3-tiny.weights'),
    ]
    for path in files:
        download_file(nextcloud_folder + path[-1], os.path.join(*path))


def main():
    download_large_files()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
