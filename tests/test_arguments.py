import pytest
import arguments
from constants import DEFAULT_BITRATE


def test_no_dir(capsys):
    with pytest.raises(SystemExit):
        arguments.parser([])
    out, err = capsys.readouterr()
    assert "error: the following arguments are required: -d/--directory" in err


def test_single_dir():
    args = arguments.parser(["-d", "~/Videos/"])
    assert args.paths == ["~/Videos/"]


def test_codec_default():
    args = arguments.parser(["-d", "~/Videos/"])
    assert args.videocodec == "hevc"


def test_codec_hevc():
    args = arguments.parser(["-d", "~/Videos/", "-c", "hevc"])
    assert args.videocodec == "hevc"


def test_codec_h264():
    args = arguments.parser(["-d", "~/Videos/", "-c", "h264"])
    assert args.videocodec == "h264"


def test_codec_wrong_choice(capsys):
    with pytest.raises(SystemExit):
        arguments.parser(["-d", "~/Videos/", "-c", "notacodec"])
    out, err = capsys.readouterr()
    assert "error: argument -c/--codec: invalid choice: 'notacodec' (choose from" in err


def test_bitrate_default():
    args = arguments.parser(["-d", "~/Videos/"])
    assert args.bitrate == DEFAULT_BITRATE


def test_bitrate_set():
    args = arguments.parser(["-d", "~/Videos/", "-b", "{}".format(int(DEFAULT_BITRATE / 2))])
    assert args.bitrate == int(DEFAULT_BITRATE / 2)


def test_bitrate_string(capsys):
    with pytest.raises(SystemExit):
        arguments.parser(["-d", "~/Videos/", "-b", "notanint"])
    out, err = capsys.readouterr()
    assert "error: argument -b/--bitrate: invalid int value: 'notanint'" in err
