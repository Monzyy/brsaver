from video import Video
import argparse
import os
import re
import subprocess
import sys

MIN_FFMPEG = "ffmpeg version 2.8"
MIN_PYTHON = (3, 5, 0)

parser = argparse.ArgumentParser(description=("Convert .mkv and .mp4 files "
                                              "to a lower bitrate to save disk space."))
parser.add_argument("-d", "--directory", dest="paths",
                    metavar="PATH", action="store", nargs="*",
                    help="path to folder containing video files",
                    type=str, required=True)
parser.add_argument("-b", "--bitrate", dest="bitrate",
                    metavar="BITRATE", action="store",
                    help="bitrate to convert video files to",
                    type=int, default=8192)
args = parser.parse_args()


def check_python_version():
    if not sys.version_info >= MIN_PYTHON:
        exit("python 3.5+ not found")


def check_ffmpeg_version():
    out = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE)
    if not MIN_FFMPEG.encode() in out.stdout:
        exit("ffmpeg version 2.8+ not found")


def collect_video_files(path):
    files = [os.path.join(root, name)
             for root, dirs, files in os.walk(path)
             for name in files
             if name.endswith((".mkv", ".mp4"))]
    return files

def main(args):
    check_python_version()
    check_ffmpeg_version()

    bitrate_target = args.bitrate
    max_bitrate = bitrate_target + 1000

    for path in args.paths:
        # Create video objects from the videofile names
        video_files = collect_video_files(path)
        videos = []
        for video_file in video_files:
            videos.append(Video(video_file))

        # Run ffmpeg -i [videofile] to get bitrates
        fileIndex = 0
        for file in video_files:
            out = subprocess.run(["ffmpeg", "-i", file], stderr=subprocess.PIPE)
            lines = out.stderr.splitlines()
            for line in lines:
                li = line.decode("utf-8")
                if "bitrate" in li:
                    videos[fileIndex].bitrate_kbps = int(re.findall(r"[\d+']+", li)[-1])
            fileIndex += 1

    # Create lower bitrate videos, if the videos bitrate is higher than max_bitrate
    for video in videos:
        if video.bitrate_kbps > max_bitrate and video.bitrate_kbps != 0:
            subprocess.run(["ffmpeg", "-y", "-i", video.fullpath, "-b:v",
                            str(bitrate_target) + "k",
                            video.directory+ "/new" + video.name + video.format])


if __name__ == "__main__":
    main(args)
