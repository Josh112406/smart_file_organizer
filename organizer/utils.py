import os
import shutil

def create_folder(folder_path) -> None:
    folder_names = ["Images", "Videos", "Audios", "Documents", "Code", "Others", "Duplicates"]
    for folder in folder_names:
        path = os.path.join(folder_path, folder)
        os.makedirs(path, exist_ok=True)
        
def get_safe_destination(dest_path: str) -> str:

    if not os.path.exists(dest_path):
        return dest_path

    directory, filename = os.path.split(dest_path)
    name, ext = os.path.splitext(filename)

    counter = 1
    while True:
        new_name = f"{name}({counter}){ext}"
        new_path = os.path.join(directory, new_name)

        if not os.path.exists(new_path):
            return new_path

        counter += 1
        
def move_file(file_source: str, file_dest: str):
    safe_dest = get_safe_destination(file_dest)
    shutil.move(file_source, safe_dest)
    
    