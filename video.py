class Video:
    name = ""
    path = ""
    file_format = ""
    bytes = 0
    seconds = 0
    bitrate_kbps = 0

    def __init__(self, path):
        self.path = path
        self.name = path.split("/")[-1]
        self.file_format = self.name.split(".")[-1]

    def __repr__(self):
        return "{}:{}".format(self.name, self.bitrate_kbps)
