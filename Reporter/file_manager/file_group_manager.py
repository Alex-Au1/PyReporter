from .file_manager import FileManager
from ..exceptions.file_except import NonExistentFileError
from typing import List


# FileGroupManager: Manages a group of files
class FileGroupManager():
    def __init__(self, file_managers: List[FileManager]):
        self._file_managers = file_managers


    # copy(): Copies a group of files from '_src' to '_dest'
    def copy(self):
        for f in self._file_managers:
            try:
                f.copy()
            except NonExistentFileError as e:
                pass
