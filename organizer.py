import shutil
import os
import exceptions as e
import utils
import json

class FileOrganizer:
    def __init__(self, folder_path: str = "."):
        self.folder_path = folder_path

    def list_files(self) -> list:
        #list all files from the given folder_path
        try:
            list_directory = os.listdir(self.folder_path)
            file_list = [file for file in list_directory if os.path.isfile(file)]
            utils.create_folder(self.folder_path)
            return file_list
        except (FileNotFoundError, OSError):
            raise e.FolderNotFound()
    
    def reverse_lookup(self, dictionary, value):
        for key, val in dictionary.items():
            if value in val: 
                print(key)
                return key
            
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
        return categorized
    
    def organize(self):
        pass
fo = FileOrganizer()
files = fo.list_files()
fo.categorize_file(files)