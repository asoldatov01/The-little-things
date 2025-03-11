import os
import shutil


current_folder = os.getcwd()

mp4_folder = os.path.join(current_folder, "mp4_files")

if not os.path.exists(mp4_folder):
    os.makedirs(mp4_folder)

for filename in os.listdir(current_folder):
    if filename.endswith(".mp4"):
        file_path = os.path.join(current_folder, filename)

        new_file_path = os.path.join(mp4_folder, filename)

        shutil.move(file_path, new_file_path)
        print(f"Файл {filename} перенесён в папку {mp4_folder}")
