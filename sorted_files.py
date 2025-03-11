import os
import shutil


current_folder = os.getcwd()


folders = {
    "photos": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
    "videos": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"],
    "audio": [".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a"],
}


for folder_name in folders.keys():
    folder_path = os.path.join(current_folder, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

for filename in os.listdir(current_folder):
    file_path = os.path.join(current_folder, filename)

    if os.path.isdir(file_path):
        continue

    file_extension = os.path.splitext(filename)[1].lower()

    moved = False
    for folder_name, extensions in folders.items():
        if file_extension in extensions:
            destination_folder = os.path.join(
                current_folder, folder_name
            )
            shutil.move(
                file_path, os.path.join(destination_folder, filename)
            )

            print(f"Файл {filename} перенесён в папку {folder_name}")

            moved = True

            break

    if not moved:
        print(f"Файл {filename} не был перемещён (неизвестный формат).")
