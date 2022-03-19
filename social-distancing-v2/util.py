import os
import urllib.request


def download_file(url, filename):
    if os.path.exists(filename):
        print("File already exists: {}".format(filename))
        return
    print("Downloading {} to {}".format(url, filename))
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, filename)
