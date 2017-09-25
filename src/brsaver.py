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


def intersperse(lst, item):
    result = [item] * (len(lst) * 2)
    result[1::2] = lst
    return result


def main(args):
    check_python_version()
    check_ffmpeg_version()
    videocodec = check_videocodec()

    bitrate_target = args.bitrate
    max_bitrate = bitrate_target + 1024

    videos = []
    video_files = collect_video_files(args.paths)
    # Create video objects from the video file names
    for video_file in video_files:
        videos.append(Video(video_file))

    # Run ffmpeg -i [videofile] to get bitrates
    fileIndex = 0
    for video in videos:
        out = subprocess.run(["ffmpeg", "-i", video.fullpath], stderr=subprocess.PIPE)
        lines = out.stderr.splitlines()
        for line in lines:
            li = line.decode("utf-8")
            if "bitrate" in li:
                video.bitrate_kbps = int(re.findall(r"[\d+']+", li)[-1])

            if "Stream" in li:
                video.streams.append(li[12:-len(li)+15])
        fileIndex += 1

    # Create lower bitrate videos, if the videos bitrate is higher than max_bitrate
    for video in videos:
        if video.bitrate_kbps > max_bitrate:
            streams = intersperse(video.streams, "-map")
            command = ["ffmpeg", "-y", "-i", video.fullpath, "-c:v", videocodec, "-b:v", str(bitrate_target) + "k",
                       "-c:a", "copy", "-c:s", "copy"]
            command.extend(streams)
            command.extend([video.directory + "/new" + video.name + video.format])
            subprocess.run(command)


if __name__ == "__main__":
    args = arguments.parser(sys.argv[1:])
    main(args)
