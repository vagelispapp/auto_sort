import shutil
from datetime import date
import os
import tkinter as tk
from tkinter import messagebox


DESTINATION = os.getcwd()
SOURCE = os.getcwd()
all_files = os.listdir(DESTINATION)
# remove script from the list
try:
    all_files.remove("auto_sort.exe")
except:
    print("No such file")

# list of file types categorized
file_types = {
    "Document & Text Files": [
        "txt",
        "csv",
        "tsv",
        "json",
        "xml",
        "yaml",
        "yml",
        "ini",
        "log",
        "md",
        "pdf",
        "docx",
        "odt",
    ],
    "Image Files": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "svg"],
    "Audio Files": ["mp3", "wav", "ogg", "flac", "m4a", "aac"],
    "Video Files": ["mp4", "avi", "mov", "mkv", "wmv", "flv", "webm"],
    "Archive & Compressed Files": [
        "zip",
        "tar",
        "tar.gz",
        "tar.bz2",
        "rar",
        "7z",
        "gz",
    ],
    "Python & Code Files": ["py", "pyc", "pyo", "ipynb", "pyd", "whl"],
    "Data & Scientific Files": [
        "xls",
        "xlsx",
        "xlsm",
        "ods",
        "db",
        "sqlite",
        "hdf5",
        "h5",
        "parquet",
        "feather",
        "pkl",
        "pickle",
        "npz",
        "npy",
    ],
    "Web Files": ["html", "htm", "css", "js", "php", "asp"],
    "Executable Files": ["exe", "dll", "bin", "dat", "conf"],
}


def get_category_for_file_type(file_type, categories):
    for category, file_types in categories.items():
        if file_type in file_types:
            return category
    return "Unknown"


root = tk.Tk()
root.withdraw()  # Hide the root window

proceed = messagebox.askyesno(
    title="Confirm File Sorting",
    message="This action will automatically sort your files into folders.\nAre you sure you want to proceed?",
)

if proceed:
    # proceed with sorting

    today = date.today()
    date_format = f"{(today).day}-{(today).month}-{(today).year}"

    # make a folder with date as name
    if date_format not in os.listdir(DESTINATION):
        try:
            os.mkdir(f"{DESTINATION}/{date_format}")
        except FileExistsError:
            print(f"Folder {date_format} already exists")

    # make a folder with category as name
    for f_category in file_types.keys():
        try:
            os.mkdir(f"{DESTINATION}/{date_format}/{f_category}")
        except FileExistsError:
            print(f"Folder {f_category} already exists")

    # move file to their folders
    for f in all_files:
        # ignore folders
        if not "." in f:
            continue

        file_type = f.split(".")[-1]
        category = get_category_for_file_type(file_type, file_types)
        if category == "Unknown":
            continue
        shutil.move(f"{SOURCE}/{f}", f"{DESTINATION}/{date_format}/{category}/{f}")

    # delete empty folders
    for folder in os.listdir(f"{DESTINATION}/{date_format}"):
        try:
            os.rmdir(f"{DESTINATION}/{date_format}/{folder}")
        except OSError:
            continue
    messagebox.showinfo(
        title="Sorting Complete", message="Your files have been successfully sorted."
    )
else:
    messagebox.showwarning("Warning", "Sorting Cancelled!")
