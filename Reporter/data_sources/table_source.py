import pandas as pd
from .df_processor import DFProcessor
from .abs_source import AbsSource
from typing import Union, Optional, List, Dict, Any


# TableSource: Class for creating custom tables
class TableSource(AbsSource):
    def __init__(self, lst_of_dict: List[Dict[Any, Any]], post_processor: Optional[DFProcessor] = None):
        super().__init__(post_processor)
        self.src = lst_of_dict


    # import_data(): Creates the custom table
    def import_data(self) -> pd.DataFrame:
        return pd.DataFrame(self.src)
