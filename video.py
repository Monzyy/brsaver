import os
class Video:
    name = ""
    path = ""
    format = ""
    bytes = 0
    seconds = 0
    bitrate_kbps = 0

    def __init__(self, path, name, format):
        self.path = path

    def __init__(self, path):
        self.path = path
        tmp = path.split('/')[-1]
        self.name = os.path.splitext(tmp)[0]
        self.format = os.path.splitext(tmp)[1]

