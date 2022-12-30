from ..abs_source import AbsSource
from selenium import webdriver
from typing import Optional, Union, Dict
from ...tools import DriverTools
from ..df_processor import DFProcessor


# WebSource: Class for importing data from a certain web location
class WebSource(AbsSource):
    def __init__(self, driver: webdriver, post_processor: Optional[Union[Dict[str, DFProcessor], DFProcessor]] = None):
        super().__init__(post_processor)
        self._driver = driver
        self._driver_tools = DriverTools(self._driver)
