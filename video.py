class Video:
    name = ""
    path = ""
    format = ""
    bytes = 0
    seconds = 0
    bitrate_kbps = 0

    def __init__(self, path):
        self.path = path
        tmp = path.split('/')[-1]
        self.name = tmp.split('.')[0]
        self.format = tmp.split('.')[1]
