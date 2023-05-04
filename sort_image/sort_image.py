from distutils.log import error

from PIL import Image
from PIL.ExifTags import TAGS


def basic_info_image(path_image):
    image = Image.open(path_image)
    info_dict = {
        "Filename": image.filename,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }
    print("=======================Basic info=======================")
    for label, value in info_dict.items():
        print(f"{label:25}: {value}")


def check_if_image_have_metadata(image_element):
    try:
        image = Image.open(image_element)
        if image.getexif():  # extract EXIF data
            return image.getexif()
    except:
        return error("no")


def metadata_image(path):
    if type(path) is list:
        for element in path:
            try:
                image = Image.open(element)
                try:
                    exifdata = image.getexif()
                    print("=======================Meta Data=======================")
                    for tag_id in exifdata:
                        tag = TAGS.get(tag_id, tag_id)
                        data = exifdata.get(tag_id)
                        if isinstance(data, bytes):
                            data = data.decode("utf-16")
                        print(f"{tag:25}: {data}")
                    print("=======================Year Date=======================")
                    year = int(exifdata[306][:4])
                    years = list(range(2021, 2025, 1))
                    if year in years:
                        print(year)
                        print(
                            "=========================  OK  ========================")
                    else:
                        print(
                            "======================== NOPE =========================")
                except:
                    print("sh1")
                    print(element)
            except:
                print("sh2")
                print(element)


def name_file_in_folder(path_folder):
    import os
    dir_path = path_folder
    name_ext = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            name_ext.append(path)
    return name_ext


def remove_metadata(path_image, final_name):
    image = Image.open(path_image)
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    image_without_exif.save(final_name)


if __name__ == "__main__":

    import os

    import numpy as np

    # FOLDER = r"D:\\"
    # list_name = name_file_in_folder(FOLDER)
    # metadata_image(list_name)

    a = check_if_image_have_metadata("a.jpg")
    print(a)

    image = Image.open("w.jpg")
    exifdata = image.getexif()
    check_if_image_have_metadata(exifdata)

    print(exifdata)
    print("=======================Meta Data=======================")
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        if isinstance(data, bytes):
            print("=======================Bytes Dec=======================")
            data = data.decode("utf-16")
        print(f"{tag:25}: {data}")
