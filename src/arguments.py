import argparse
from constants import VIDEO_CODECS
from constants import DEFAULT_BITRATE


def parser(args):
    parser = argparse.ArgumentParser(description=("Convert .mkv and .mp4 files "
                                                  "to a lower bitrate to save disk space."))
    parser.add_argument("-d", "--directory", dest="paths",
                        metavar="PATH", action="store", nargs="*",
                        help="path to folder containing video files",
                        required=True)
    parser.add_argument("-c", "--codec", dest="videocodec",
                        metavar="VIDEOCODEC", action="store",
                        help="videocodec to encode to (default: hevc)",
                        type=str, default="hevc", choices=VIDEO_CODECS)
    parser.add_argument("-b", "--bitrate", dest="bitrate",
                        metavar="BITRATE", action="store",
                        help="bitrate to convert video files to in kbit",
                        type=int, default=DEFAULT_BITRATE)
    return parser.parse_args(args)
