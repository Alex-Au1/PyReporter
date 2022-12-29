import pandas as pd
import copy
from ..tools import DataFrameTools as DfTools
from .abs_source_data_frame import AbsSourceDf


# ExcelDf: Class to store dataframe sources for an excel
class ExcelDf(AbsSourceDf):
    def __init__(self, df: pd.DataFrame, startrow: int = 0, startcol: int = 0, with_headers: bool = True, src_to_celled: bool = True):
        super().__init__(df)

        # if we need to convert each datacell in the source data frame to a Cell object
        if (src_to_celled):
            self.df = DfTools.df_to_celled_df(self.df)

        self.display_df = copy.deepcopy(self.df)
        self.display_df = DfTools.celled_df_to_display_df(self.display_df)

        # left hand corner position of the dataframe
        self.startrow = startrow
        self.startcol = startcol

        # flags for including the header of the dataframe
        self.with_headers = with_headers
