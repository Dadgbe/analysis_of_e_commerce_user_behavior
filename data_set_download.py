# data_set_download.py

import os
import kagglehub
import shutil

os.makedirs("data_raw", exist_ok=True)
os.chdir("data_raw")

archive_path = kagglehub.dataset_download(
    "mkechinov/ecommerce-behavior-data-from-multi-category-store"
)
print("Downloaded to cache:", archive_path)

def copy_or_unpack(src, dest_dir="."):
    if os.path.isdir(src):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dest_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        print(f"Copied contents of directory {src} into {dest_dir}")
    else:
        shutil.unpack_archive(src, extract_dir=dest_dir)
        print(f"Unpacked archive {src} into {dest_dir}")

copy_or_unpack(archive_path, dest_dir=".")

print("Current data_raw/ contents:", os.listdir("."))

os.chdir("..")
