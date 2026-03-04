class Error(Exception):
    """Base class for exceptions"""

class FolderNotFound(Error):
    """Raised when folder does not exist"""

    def __init__(self, msg='Folder not found.') -> None:
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        return self.msg