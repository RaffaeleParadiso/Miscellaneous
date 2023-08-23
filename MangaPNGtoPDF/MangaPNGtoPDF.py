"""
Convert all high quality png files downloaded from mangaworld to pdf separated by chapter

"""


import glob
import os
import re

from PIL import Image


def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders


if __name__ == '__main__':

    directory = fast_scandir(os.getcwd())

    manga = ["Boku no Hero Academia", "Jujutsu Kaisen",
             "One Piece", "One Punch-Man", "Chainsaw Man"]
    for mg in manga:
        rootdir = f'c:\\Users\\raffa\\Downloads\\{mg}'
        for subdir, _, _ in os.walk(rootdir):
            for dirpath, dirnames, filenames in os.walk(subdir):
                dirr = [(os.path.join(rootdir, dir)) for dir in dirnames]
                for element in dirr:
                    cap = re.findall(r'\d+', str(element))
                    files = (os.listdir(element))
                    images = [Image.open(os.path.join(element, filename))
                              for filename in files if not filename.endswith('.pdf')]
                    im = [image.convert('RGB') for image in images]
                    os.makedirs(f'{mg}/PDF', exist_ok=True)
                    if len(cap) == 1:
                        if os.path.isfile(f'c:\\Users\\raffa\\Downloads\\{mg}\\PDF\\{cap[0]}.pdf') == False:
                            im[0].save(f'{mg}/PDF/{cap[0]}.pdf',
                                       save_all=True, append_images=im[1:])
                            print(f"{cap[0]} - {mg} Created")
                        else:
                            print(f"{cap[0]} - {mg} Exist")
                    if len(cap) == 2:
                        if os.path.isfile(f'c:\\Users\\raffa\\Downloads\\{mg}\\PDF\\{cap[0]}.{cap[1]}.pdf') == False:
                            im[0].save(f'{mg}/PDF/{cap[0]}.{cap[1]}.pdf',
                                       save_all=True, append_images=im[1:])
                            print(f"{cap[0]}.{cap[1]} - {mg} Created")
                        else:
                            print(f"{cap[0]}.{cap[1]} - {mg} Exist")
