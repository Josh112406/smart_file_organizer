# Smart File Organizer

A command-line tool that automatically organizes files in a folder by category and detects duplicates.

## Features

- Sorts files into categorized folders: **Images**, **Videos**, **Audios**, **Documents**, **Code**, and **Others**
- Detects duplicate files using SHA-256 hashing and moves them to a **Duplicates** folder
- Handles filename conflicts by appending a counter (e.g., `photo(1).jpg`)
- Prints an organization summary after completion

## Usage

```bash
python file_organizer.py <path_to_folder>
```

### Example

```bash
python file_organizer.py C:\Users\me\Downloads
```

Output:

```
Organization Summary
--------------------
Files processed : 25
Files moved     : 25
Duplicates      : 3
```

## Supported File Types

| Category    | Extensions                                                                 |
|-------------|---------------------------------------------------------------------------|
| Images      | jpg, jpeg, png, gif, bmp, tiff, webp, svg, heic, raw, ico, psd, ai, eps  |
| Videos      | mp4, mkv, avi, mov, wmv, flv, webm, m4v, 3gp, mpeg, mpg, ts             |
| Audios      | mp3, wav, aac, flac, ogg, wma, m4a, alac, aiff, opus, mid, midi         |
| Documents   | pdf, doc, docx, xls, xlsx, ppt, pptx, txt, rtf, odt, csv, tex           |
| Code        | html, css, js, ts, py, java, c, cpp, cs, php, rb, go, swift, json, yaml |

Files with unrecognized extensions are moved to **Others**.

## Project Structure

```
smart_file_organizer/
├── file_organizer.py          # Entry point
├── README.md
└── organizer/
    ├── __init__.py
    ├── organizer.py           # Core FileOrganizer class
    ├── duplicate_handler.py   # SHA-256 duplicate detection
    ├── exceptions.py          # Custom exceptions
    ├── file_types.json        # Extension-to-category mapping
    └── utils.py               # Folder creation and file moving utilities
```

## Requirements

- Python 3.11+
