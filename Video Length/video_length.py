'''
Check the lenght of all video in a directory using ffmpeg, 
install it with: "sudo apt install ffmpeg"
'''
import argparse
import subprocess
from pathlib import Path


def video_length(filename):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
         "default=noprint_wrappers=1:nokey=1", "--", filename,], capture_output=True, text=True,)
    try:
        return float(result.stdout)
    except ValueError:
        raise ValueError(result.stderr.rstrip("\n"))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find lenght of all video in a directory.')
    parser.add_argument('-d', '--dir', required=True,
                        help='Pass the full path of the directory.')
    parser.add_argument('-e', '--ext', required=True, nargs='*',
                        help='Pass the extension. Example "python lenghtvideo.py -d /home/user/ -e mkv mp4"')

    args = parser.parse_args()
    directory = args.dir
    extension = args.ext

    if directory:
        hours = 0
        for element in extension:
            dur = sum(video_length(f)
                      for f in Path(f"{directory}").rglob(f"*.{element}"))
            hours = hours + dur
            # mkv = sum(video_length(f) for f in Path(f"{directory}").rglob("*.mkv"))
        print(f"{((hours)/3600):.1f} hours")
