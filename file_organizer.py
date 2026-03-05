import argparse
from organizer.organizer import FileOrganizer
from organizer.duplicate_handler import DuplicateHandler

def main():
    parser = argparse.ArgumentParser(
        description="Organize files in folder by category and detect duplicates."
    )
    
    parser.add_argument("path", help="Path to the folder you want to organize.")
    args = parser.parse_args()
    duplicate_handler = DuplicateHandler()
    organizer = FileOrganizer(args.path, duplicate_handler)
    
    organizer.organize()
    organizer.print_summary()

if __name__ == "__main__":
    main()