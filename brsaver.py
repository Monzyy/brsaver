from video import Video
import argparse
import os
import re
import subprocess


parser = argparse.ArgumentParser(description=('Convert .mkv and .mp4 files '
                                              'to a lower bitrate to save disk space.'))
parser.add_argument('-d', '--directory', dest='path',
                    metavar='PATH', action='store',
                    help='path to folder containing video files',
                    type=str, required=True)
parser.add_argument('-b', '--bitrate', dest='bitrate',
                    metavar='BITRATE', action='store',
                    help='bitrate to convert video files to',
                    type=int, default=8192)
args = parser.parse_args()


def main(args):
    bitrate_target = args.bitrate
    max_bitrate = bitrate_target + 1000
    path = args.path

    # Get all videofiles with proper filetypes from the folder and all subfolders
    vfiles = [os.path.join(root, name)
              for root, dirs, files in os.walk(path)
              for name in files
              if name.endswith((".mkv", ".mp4"))]

    videos = []

    # Create video objects from the videofile names
    for vfile in vfiles:
        videos.append(Video(vfile))


    fileIndex = 0

    # Run ffmpeg -i [videofile] to get bitrates
    for file in vfiles:
        tmp = subprocess.run(["ffmpeg", "-i", file], stderr=subprocess.PIPE)
        lines = tmp.stderr.splitlines()
        for line in lines:
            li = line.decode("utf-8")
            if "bitrate" in li:
                videos[fileIndex].bitrate_kbps = int(re.findall(r"[\d+']+", li)[-1])
        fileIndex += 1

    # Create lower bitrate videos, if the videos bitrate is higher than max_bitrate
    for video in videos:
        if video.bitrate_kbps > max_bitrate and video.bitrate_kbps != 0:
            subprocess.run(["ffmpeg", "-y", "-i", video.path, "-b:v",
                            str(bitrate_target) + "k",
                            path + "new" + video.name + video.format])


if __name__ == '__main__':
    main(args)
