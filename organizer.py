import os
import exceptions as e
import utils
import json
from duplicate_handler import DuplicateHandler
class FileOrganizer:
    def __init__(self, folder_path: str, duplicate_handler):
        self.folder_path = folder_path
        self.duplicate_handler = duplicate_handler
        
    def scan_directory(self) -> list:
        #list all files from the given folder_path
        try:
            list_directory = os.listdir(self.folder_path)
            file_list = [file for file in list_directory if os.path.isfile(os.path.join(self.folder_path, file))]
            utils.create_folder(self.folder_path)
            return file_list
        except (FileNotFoundError, OSError) as er:
            raise e.FolderNotFound()
            
    def categorize_file(self, file_list: list) -> dict:
        #check file type
        if not file_list:
            print("No file found.")
            return
        
        categorized = {}
        with open("file_types.json", "r") as f:
            file_types = json.load(f)
        
        for file in file_list:
            found_category = False
            extension = os.path.splitext(file)[1].strip('.')
            for category, extensions in file_types.items():
                if extension in [ext.lower() for ext in extensions]:
                    categorized[file] = category
                    found_category = True
                    break
                
            if not found_category:
                categorized[file] = "others"
        return categorized
    
    def organize(self):
        files = self.scan_directory()
        categorized = self.categorize_file(files)
        
        for file_name, category in categorized.items():
            file_path = os.path.join(self.folder_path, file_name)
            # duplicate check
            if self.duplicate_handler.is_duplicate(file_path):
                dest_folder = "Duplicates"
            else:
                if category == "images":
                    dest_folder = "Images"
                elif category == "audio":
                    dest_folder = "Audio"
                elif category == "videos":
                    dest_folder = "Videos"
                elif category == "documents":
                    dest_folder = "Documents"
                elif category == "code":
                    dest_folder = "Code"
                else:
                    dest_folder = "Others"
                
            dest_path = os.path.join(self.folder_path, dest_folder,file_name)
            source_path = os.path.join(self.folder_path, file_name)
            utils.move_file(source_path, dest_path)
            
    def main():
        folder_path = input("Enter folder path: ")
        duplicate_handler = DuplicateHandler()
        organizer = FileOrganizer(folder_path, duplicate_handler)
        organizer.organize()        
