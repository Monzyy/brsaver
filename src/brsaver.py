from video import Video
import arguments
import os
import re
import subprocess
import sys
from constants import MIN_PYTHON
from constants import MIN_FFMPEG
from constants import VIDEO_CODECS


def check_python_version():
    if not sys.version_info >= MIN_PYTHON:
        exit("python 3.5+ not found")


def check_ffmpeg_version():
    out = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE)
    if not MIN_FFMPEG.encode() in out.stdout:
        exit("ffmpeg not found")


def check_videocodec():
    videocodec = args.videocodec.lower()
    if videocodec in VIDEO_CODECS:
        return videocodec
    else:
        exit(args.videocodec + " is not a supported videocodec")


def collect_video_files(paths):
    files = [os.path.join(root, name)
             for path in paths
             for root, dirs, files in os.walk(path)
             for name in files
             if name.endswith((".mkv", ".mp4"))]
    return files


def main(args):
    check_python_version()
    check_ffmpeg_version()
    videocodec = check_videocodec()

    bitrate_target = args.bitrate
    max_bitrate = bitrate_target + 1000

    videos = []
    video_files = collect_video_files(args.paths)
    # Create video objects from the videofile names
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
        if video.bitrate_kbps > max_bitrate:
            subprocess.run(["ffmpeg", "-y", "-i", video.fullpath, "-c:v", videocodec, "-b:v",
                            str(bitrate_target) + "k",
                            video.directory + "/new" + video.name + video.format])


if __name__ == "__main__":
    args = arguments.parser(sys.argv[1:])
    main(args)
