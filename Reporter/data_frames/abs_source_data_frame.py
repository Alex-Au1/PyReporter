import pandas as pd
import copy
from ..tools import DataFrameTools as DfTools


# ExcelDf: Class to store dataframe sources for a generic source
class AbsSourceDf():
    def __init__(self, df: pd.DataFrame):
        self.df = df
