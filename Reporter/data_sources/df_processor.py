import pandas as pd
import numpy as np
from ..tools import DataFrameTools as DfTools
from typing import Optional, List, Dict


# DFProcessor: Used to process the imported dataframe
# Note: -This processor will
#           1. select only a subset of the dataframe indicated based off the indicated boundaries
#           2. drop columns with all nan values
#           3. rename columns by name
#           4. rename columns by index
#           5. select needed columns
#           6. change data types
#           7. filter rows based off distinct columns
#       - 'renamed columns' has the format of:  {old_name: new_name, ...}
#       - 'changed_dtypes' has the format of: {col_name: dtype}
#           the dtypes should be the dtypes used for pandas.Series based off the documentation.
#           These dtypes should be the same as the dtypes from numpy library
class DFProcessor():
    def __init__(self, top: Optional[int] = None, bottom: Optional[int] = None, left: Optional[int] = None, right: Optional[int] = None , renamed_columns : Dict[str, str]= {}, ind_renamed_columns: Dict[int, str] = {}, selected_columns: Optional[List[str]] = None,
                 changed_dtypes: Dict[str, str] = {}, distinct_columns: Optional[List[str]] = None, drop_empty_columns: bool = False, replace_nan: bool = True):
        self.__top = top
        self.__bottom = bottom
        self.__left = left
        self.__right = right
        self.__renamed_columns = renamed_columns
        self.__ind_renamed_columns = ind_renamed_columns
        self.__selected_columns = selected_columns
        self.__changed_dtypes = changed_dtypes
        self.__distinct_columns = distinct_columns
        self.__drop_empty_columns = drop_empty_columns
        self.__replace_nan = replace_nan


    # crop_table(df): Chooses only a subset of 'df'
    def crop_table(self, df: pd.DataFrame) -> pd.DataFrame:
        top_specified = bool(self.__top is not None)
        bottom_specified = bool(self.__bottom is not None)
        left_specified = bool(self.__left is not None)
        right_specified = bool(self.__right is not None)

        # get the specific table
        if (top_specified and bottom_specified and left_specified and right_specified):
            df = DfTools.ind_subset(df, self.__top, self.__bottom, self.__left, self.__right)
        else:
            # remove by rows
            if (top_specified and bottom_specified):
                df = df.iloc[self.__top:self.__bottom]
            elif (top_specified):
                df = DfTools.remove_top_rows(df, self.__top)
            elif (not top_specified and bottom_specified):
                df = df.iloc[:self.__bottom]

            # remove by columns
            if (left_specified and right_specified):
                df = df.iloc[: , self.__left:self.__right]
            elif (left_specified):
                df = df.iloc[: ,self.__left: ]
            elif (not left_specified and right_specified):
                df = df.iloc[: , :self.__right]

        return df


    # change_types(df): Changes the data types of certain columns
    def change_types(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in self.__changed_dtypes:
            if (self.__changed_dtypes[col] == "numeric"):
                df[col] = pd.to_numeric(df[col])
            else:
                df[col] = pd.Series(df[col],  dtype = self.__changed_dtypes[col])

        return df


    # process(): Post processes 'df' to be used
    # Note: This processor will
    #           1. select only a subset of the dataframe indicated based off the indicated boundaries
    #           2. drop columns with all nan values
    #           3. rename columns by name
    #           4. rename columns by index
    #           5. select needed columns
    #           6. change data types
    #           7. filter rows based off distinct columns
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        # 1. crop the table by choosing which cells to select
        df = self.crop_table(df)

        # 2. drop the columns with all nan values
        if (self.__drop_empty_columns):
            df = df.dropna(axis=1, how='all')

        # 3. rename the columns by name
        df = df.rename(columns = self.__renamed_columns)

        # 4. rename the columns by index
        for col_ind in self.__ind_renamed_columns:
            df.columns.values[col_ind] = self.__ind_renamed_columns[col_ind]

        # 5. select the columns needed
        if (self.__selected_columns is not None):
            df = df[self.__selected_columns]

        # 6. change the types of the columns
        df = self.change_types(df)

        # 7. filter the rows based off the selected distinct columns
        if (self.__distinct_columns is not None):
            df = df.drop_duplicates(subset = self.__distinct_columns)


        if (self.__replace_nan):
            df = df.replace(np.nan,0)

        return df
