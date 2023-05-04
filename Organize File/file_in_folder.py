"""
moves images, videos, and audio files
"""

import os
import shutil

audio = (".3ga", ".aac", ".ac3", ".aif", ".aiff",
         ".alac", ".amr", ".ape", ".au", ".dss",
         ".flac", ".flv", ".m4a", ".m4b", ".m4p",
         ".mp3", ".mpga", ".ogg", ".oga", ".mogg",
         ".opus", ".qcp", ".tta", ".voc", ".wav",
         ".wma", ".wv")

video = (".webm", ".MTS", ".M2TS", ".TS", ".mov",
         ".mp4", ".m4p", ".m4v", ".mxf")

img = (".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp", ".png",
       ".gif", ".webp", ".svg", ".apng", ".avif")


def is_audio(file):
    return os.path.splitext(file)[1] in audio


def is_video(file):
    return os.path.splitext(file)[1] in video


def is_image(file):
    return os.path.splitext(file)[1] in img


os.chdir(os.getcwd())
path = os.getcwd()

for file in os.listdir():
    if is_audio(file):
        if f"{path}\Audio" not in os.listdir():
            try:
                os.mkdir(f"{path}\\Audio")
            except:
                pass
        shutil.move(file, f"{path}\\Audio")
    elif is_video(file):
        if f"{path}\Video" not in os.listdir():
            try:
                os.mkdir(f"{path}\\Video")
            except:
                pass
        shutil.move(file, f"{path}\\Video")
    elif is_image(file):
        if f"{path}\Images" not in os.listdir():
            try:
                os.mkdir(f"{path}\\Images")
            except:
                pass
        shutil.move(file, f"{path}\\Images")
    else:
        if f"{path}\Documents" not in os.listdir():
            try:
                os.mkdir(f"{path}\\Documents")
            except:
                pass
        shutil.move(file, f"{path}\\Documents")
