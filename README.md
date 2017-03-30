# Bitrate Saver
Convert .mkv and .mp4 files to a lower bitrate to save disk space.

## Setup
To use, first set up a virtual environment:

    $ pip install virtualenv
    $ virtualenv brsaver/
    $ cd brsaver/
    $ source bin/activate
    $ pip install -r requirements.txt
    
Leaving the virtual environment is done by writing:

    $ deactivate
    
To reactivate the virtual environment write:

    $ source bin/activate

## Usage
    $ python3 brsaver.py -d ~/Videos/ -b 8192 -c hevc
    $ python3 brsaver.py -h
