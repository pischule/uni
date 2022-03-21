import os.path
import sys
import urllib.request

from PySide6.QtWidgets import QApplication

from gui.widgets.main_window import MainWindow


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
