import shutil
import os
import exceptions as e
import utils
import json

class FileOrganizer:
    def __init__(self, folder_path: str = "./To Do"):
        self.folder_path = folder_path
    
    def scan_directory(self) -> list:
        #list all files from the given folder_path
        try:
            list_directory = os.listdir(self.folder_path)
            file_list = [file for file in list_directory if os.path.isfile(f"{self.folder_path}/{file}")]
            utils.create_folder(self.folder_path)
            return file_list
        except (FileNotFoundError, OSError):
            raise e.FolderNotFound()
            
    def categorize_file(self, file_list: list) -> dict:
        #check file type
        categorized = {}
        with open("file_types.json", "r") as f:
            file_types = json.load(f)
        
        for file in file_list:
            extension = os.path.splitext(file)[1].strip('.')
            for category, extensions in file_types.items():
                if extension in [ext.lower() for ext in extensions]:
                    categorized[file] = category
                    break
                else:
                    categorized[file] = "others"
        return categorized
    
    def organize(self):
        files = self.scan_directory()
        categorized = self.categorize_file(files)
        for file_name, category in categorized.items():
            if category == "images":
                utils.move_file(file_name, f"Images/{file_name}")
            elif category == "audio":
                utils.move_file(file_name, f"Images/{file_name}")
            elif category == "videos":
                utils.move_file(file_name, f"Videos/{file_name}")
            elif category == "documents":
                utils.move_file(file_name, f"Documents/{file_name}")
            elif category == "code":
                utils.move_file(file_name, f"Code/{file_name}")
            else:
                utils.move_file(file_name, f"Others/{file_name}")
                
fo = FileOrganizer()
fo.scan_directory()