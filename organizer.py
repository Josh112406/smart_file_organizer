import shutil
import os
import exceptions as e
import utils
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
        
    def check_type(self, file_list: list):
        #check file type
        pass
    
    def organize(self):
        pass
file = FileOrganizer().list_files()