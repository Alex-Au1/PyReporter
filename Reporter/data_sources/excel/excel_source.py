from ..file_source import FileSource
import pandas as pd
from ..sharepoint import SharePoint
from pathlib import Path
import io
from ..df_processor import DFProcessor
from typing import Optional, Union, Dict


# ExcelSource: Imports a table from excel
class ExcelSource(FileSource):
    def __init__(self, path: str, sheet: Optional[str] = None, from_sharepoint: bool = False,
                 sharepoint: Optional[SharePoint] = None, post_processor: Optional[Union[Dict[str, DFProcessor], DFProcessor]] = None):
        super().__init__(path, post_processor)
        self._sheet = sheet

        # default to get first sheet if the sheet is not specified
        if (self._sheet is None):
            self._sheet = 0

        self._from_sharepoint = from_sharepoint
        self._sharepoint = sharepoint
        self._engine = "openpyxl"


    # sheet(): Getter for '_sheet'
    @property
    def sheet(self):
        return self._sheet


    # sheet(): Setter for '_sheet'
    @sheet.setter
    def sheet(self, new_sheet):
        self._sheet = new_sheet


    # import_data(): Imports the table from excel
    async def import_data(self) -> pd.DataFrame:
        # open from local file path
        if (self._sharepoint is None):
            df = pd.read_excel(self._path, sheet_name = self._sheet, parse_dates = True)
        # open from sharepoint
        else:
            file_bytes = self._sharepoint.open_file_bytes(self._path)
            df = pd.read_excel(file_bytes, sheet_name = None, parse_dates = True)

        return df
