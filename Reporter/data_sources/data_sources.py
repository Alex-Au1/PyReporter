import pandas as pd
from .source_manager import SourceManager


# DataSources: All data sources used for a report
class DataSources():
    def __init__(self):
        self.sources = {}


    def __getitem__(self, key: str):
        return self.sources[key]


    def __setitem__(self, key: str, value: SourceManager):
        assert isinstance(value, SourceManager)
        self.sources[key] = value
