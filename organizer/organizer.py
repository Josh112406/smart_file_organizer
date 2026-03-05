import os
from . import utils
import json
from .duplicate_handler import DuplicateHandler
from exceptions import FolderNotFound

ORGANIZER_FOLDERS = {
    "Images",
    "Videos",
    "Audios",
    "Documents",
    "Code",
    "Others",
    "Duplicates",
}

CATEGORY_FOLDER_MAP = {
    "images": "Images",
    "videos": "Videos",
    "audios": "Audios",
    "documents": "Documents",
    "codes": "Code",
}


class FileOrganizer:
    def __init__(self, folder_path: str, duplicate_handler: DuplicateHandler):
        self.folder_path = folder_path
        self.duplicate_handler = duplicate_handler
        self.files_processed = 0
        self.files_moved = 0

    def scan_directory(self) -> list:
        if not os.path.isdir(self.folder_path):
            raise FolderNotFound(f"Folder not found: {self.folder_path}")

        utils.create_folder(self.folder_path)
        list_directory = os.listdir(self.folder_path)
        file_list = [
            file
            for file in list_directory
            if os.path.isfile(os.path.join(self.folder_path, file))
            and file not in ORGANIZER_FOLDERS
        ]
        return file_list

    def categorize_file(self, file_list: list) -> dict:
        if not file_list:
            print("No file found.")
            return {}

        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "file_types.json")
        categorized = {}
        with open(file_path, "r") as f:
            file_types = json.load(f)

        extension_map = {}
        for category, extensions in file_types.items():
            for ext in extensions:
                extension_map[ext.lower()] = category

        for file in file_list:
            extension = os.path.splitext(file)[1].strip(".").lower()
            categorized[file] = extension_map.get(extension, "others")
        return categorized

    def organize(self):
        files = self.scan_directory()
        categorized = self.categorize_file(files)

        for file_name, category in categorized.items():
            file_path = os.path.join(self.folder_path, file_name)
            self.files_processed += 1

            if self.duplicate_handler.is_duplicate(file_path):
                dest_folder = "Duplicates"
            else:
                dest_folder = CATEGORY_FOLDER_MAP.get(category, "Others")

            dest_path = os.path.join(self.folder_path, dest_folder, file_name)
            source_path = os.path.join(self.folder_path, file_name)
            utils.move_file(source_path, dest_path)

            self.files_moved += 1

    def print_summary(self):
        print("\nOrganization Summary")
        print("--------------------")
        print(f"Files processed : {self.files_processed}")
        print(f"Files moved     : {self.files_moved}")
        print(f"Duplicates      : {self.duplicate_handler.duplicate_count}")
