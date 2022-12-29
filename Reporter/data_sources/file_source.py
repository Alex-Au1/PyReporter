from .abs_source import AbsSource
from .df_processor import DFProcessor
import glob, enum, os
from typing import Optional


# FileExtensions: Different types of file extensions
class FileExtensions(enum.Enum):
    NewExcel = "xlsx"
    OldExcel = "xls"


# FileSource: Class for a source from a file
class FileSource(AbsSource):
    def __init__(self, path: str, post_processor: Optional[DFProcessor] = None):
        super().__init__(post_processor)
        self._path = path


    # path(): Getter for 'path'
    @property
    def path(self):
        return self._path


    # path(): Setter to check if 'new_path' exists
    @path.setter
    def path(self, new_path: str):
        glob_result = glob.glob(new_path)

        # get the latest file if we have multiple files that match the globbing result
        if (glob_result):
            latest_file = max(glob_result, key=os.path.getctime)
            self._path = latest_file
