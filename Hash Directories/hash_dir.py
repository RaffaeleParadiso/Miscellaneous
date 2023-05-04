""" Check if two folders have the same md5 hash """
import argparse
import hashlib
import tkinter as tk
from functools import partial
from pathlib import Path
from typing import Union

from _hashlib import HASH as Hash


def md5_update_from_file(filename: Union[str, Path], hash: Hash) -> Hash:
    assert Path(filename).is_file()
    with open(str(filename), "rb") as f:
        for chunk in iter(lambda: f.read(512), b""):
            hash.update(chunk)
    return hash


def md5_file(filename: Union[str, Path]) -> str:
    return str(md5_update_from_file(filename, hashlib.md5()).hexdigest())


def md5_update_from_dir(directory: Union[str, Path], hash: Hash) -> Hash:
    assert Path(directory).is_dir()
    for path in sorted(Path(directory).iterdir(), key=lambda p: str(p).lower()):
        hash.update(path.name.encode())
        if path.is_file():
            hash = md5_update_from_file(path, hash)
        elif path.is_dir():
            hash = md5_update_from_dir(path, hash)
    return hash


def md5_dir(directory: Union[str, Path]) -> str:
    return str(md5_update_from_dir(directory, hashlib.md5()).hexdigest())


def md5(n, m):
    a = md5_dir(n)
    b = md5_dir(m)
    if a != b:
        return ("Different Hash")
    else:
        return("Same Hash")


def call_result(label_result, n1, n2):
    num1 = (n1.get())
    num2 = (n2.get())
    result = md5(num1, num2)
    return label_result.config(text=f"Result = {result}")


def call_result_ng(num1, num2):
    result = md5(num1, num2)
    print(f"Result = {result}")


parser = argparse.ArgumentParser(description='Gui Digest')
parser.add_argument('-g', '--gui', action='store_true',
                    help='show gui interface')

args = parser.parse_args()
gui = args.gui
if gui:
    root = tk.Tk()
    root.geometry('400x200')
    root.title("Welcome to MD5 Hash Dir!")
    number1 = tk.StringVar()
    number2 = tk.StringVar()
    labelNum1 = tk.Label(root, text="First Directory").grid(row=1, column=0)
    labelNum2 = tk.Label(root, text="Second Directory").grid(row=2, column=0)
    labelResult = tk.Label(root)
    labelResult.grid(row=20, column=2)
    entryNum1 = tk.Entry(root, textvariable=number1).grid(row=1, column=2)
    entryNum2 = tk.Entry(root, textvariable=number2).grid(row=2, column=2)
    call_result = partial(call_result, labelResult, number1, number2)
    buttonCal = tk.Button(root, text="Calculate",
                          command=call_result).grid(row=3, column=2)
    root.mainloop()
else:
    number1 = input('First directory: \n')
    number2 = input('Second directory: \n')
    call_result_ng(number1, number2)
