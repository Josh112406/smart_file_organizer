import os
import shutil

def create_folder(folder_path) -> None:
    folder_names = ["Images", "Videos", "Audios", "Documents", "Code", "Others"]
    for folder in folder_names:
        if not os.path.exists(f"{folder_path}/{folder}"):
            os.mkdir(f"{folder_path}/{folder}")
        
def move_file(file_source: str, file_dest: str):
    shutil.move(file_source, file_dest)