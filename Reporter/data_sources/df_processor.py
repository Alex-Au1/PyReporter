import pandas as pd
import numpy as np
from collections import defaultdict
from ..tools import DataFrameTools as DfTools
from typing import Optional, List, Dict, Any

DISTINCT_KEEP_VALS = ["first", "last"]
DEFAULT_DISTINCT = DISTINCT_KEEP_VALS[0]

# DFProcessor: Used to process the imported dataframe
# Note: -This processor will
#           1. set a specific row as the header column names
#           2. select only a subset of the dataframe indicated based off the indicated boundaries
#           3. drop columns with all nan values
#           4. rename columns by name
#           5. rename columns by index
#           6. select needed columns
#           7. change data types
#           8. filter rows based off distinct columns
#       - 'renamed columns' has the format of:  {old_name: new_name, ...}
#       - 'changed_dtypes' has the format of: {col_name: dtype}
#           the dtypes should be the dtypes used for pandas.Series based off the documentation.
#           These dtypes should be the same as the dtypes from numpy library
class DFProcessor():
    def __init__(self, header_row_pos : Optional[int] = None, top: Optional[int] = None, bottom: Optional[int] = None, left: Optional[int] = None, right: Optional[int] = None , renamed_columns : Dict[str, str]= {}, ind_renamed_columns: Dict[int, str] = {},
                 ind_selected_columns: Optional[List[int]] = None, selected_columns: Optional[List[str]] = None, changed_dtypes: Dict[str, str] = {}, distinct_columns: Optional[List[str]] = None, distinct_keep: str = DEFAULT_DISTINCT,
                 drop_empty_columns: bool = False, replace_nan: bool = True):
        self._header_row_pos = header_row_pos
        self._top = top
        self._bottom = bottom
        self._left = left
        self._right = right
        self._renamed_columns = renamed_columns
        self._ind_renamed_columns = ind_renamed_columns
        self._ind_selected_columns = ind_selected_columns
        self._selected_columns = selected_columns
        self._changed_dtypes = changed_dtypes
        self._distinct_columns = distinct_columns
        self._distinct_keep = distinct_keep
        self._drop_empty_columns = drop_empty_columns
        self._replace_nan = replace_nan


    # crop_table(df): Chooses only a subset of 'df'
    def crop_table(self, df: pd.DataFrame) -> pd.DataFrame:
        top_specified = bool(self._top is not None)
        bottom_specified = bool(self._bottom is not None)
        left_specified = bool(self._left is not None)
        right_specified = bool(self._right is not None)

        # get the specific table
        if (top_specified and bottom_specified and left_specified and right_specified):
            df = DfTools.ind_subset(df, self._top, self._bottom, self._left, self._right)
        else:
            # remove by rows
            if (top_specified and bottom_specified):
                df = df.iloc[self._top:self._bottom]
            elif (top_specified):
                df = DfTools.remove_top_rows(df, self._top)
            elif (not top_specified and bottom_specified):
                df = df.iloc[:self._bottom]

            # remove by columns
            if (left_specified and right_specified):
                df = df.iloc[: , self._left:self._right]
            elif (left_specified):
                df = df.iloc[: ,self._left: ]
            elif (not left_specified and right_specified):
                df = df.iloc[: , :self._right]

        return df


    # change_types(df): Changes the data types of certain columns
    def change_types(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in self._changed_dtypes:
            if (self._changed_dtypes[col] == "numeric"):
                df[col] = pd.to_numeric(df[col])
            else:
                df[col] = pd.Series(df[col],  dtype = self._changed_dtypes[col])

        return df


    # _col_name_to_ind(df, column_names, result): Converts 'column_names' to its
    #   corresponding indices
    # Effects: modifies 'result'
    def _col_name_to_ind(self, df: pd.DataFrame, column_names: List[Any], result: List[int]):
        columns = df.columns
        column_pos = defaultdict(list)
        pos = 0

        # bucket all the column indices
        for c in columns:
            column_pos[c].append(pos)
            pos += 1

        # retrieve the column indices from the selected column names
        for c in column_names:
            result += column_pos[c]


    # select_columns(df): Selects the needed columns
    def select_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        selected_col_ind = []
        self._col_name_to_ind(df, self._selected_columns, selected_col_ind)

        selected_col_ind += self._ind_selected_columns

        # remove duplicate column indices
        selected_col_ind = set(selected_col_ind)
        selected_col_ind = list(selected_col_ind)

        # sort the indices by the order the columns appear
        selected_col_ind.sort()

        return df.iloc[: ,selected_col_ind]


    # process(): Post processes 'df' to be used
    # Note: This processor will
    #           1. set a specific row as the header column names
    #           2. select only a subset of the dataframe indicated based off the indicated boundaries
    #           3. drop columns with all nan values
    #           4. rename columns by name
    #           5. rename columns by index
    #           6. select needed columns
    #           7. change data types
    #           8. filter rows based off distinct columns
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        # 1. set a specific row as the header column names
        if (self._header_row_pos is not None):
            columns = df.iloc[self._header_row_pos]
            df.columns = columns

        # 2. crop the table by choosing which cells to select
        df = self.crop_table(df)

        # 3. drop the columns with all nan values
        if (self._drop_empty_columns):
            df = df.dropna(axis=1, how='all')

        # 4. rename the columns by name
        df = df.rename(columns = self._renamed_columns)

        # 5. rename the columns by index
        for col_ind in self._ind_renamed_columns:
            df.columns.values[col_ind] = self._ind_renamed_columns[col_ind]

        # 6. select needed columns by index
        if (self._ind_selected_columns is not None or self._selected_columns is not None):
            df = self.select_columns(df)

        # 7. change the types of the columns
        df = self.change_types(df)

        # 8. filter the rows based off the selected distinct columns
        if (self._distinct_columns is not None):
            df = df.drop_duplicates(subset = self._distinct_columns, keep = self._distinct_keep)

        if (self._replace_nan):
            df = df.replace(np.nan,0)

        return df
