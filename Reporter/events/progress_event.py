import pandas as pd
from .out_event import OutEvent
from typing import List, Optional, Any


# DebugOutEvent: Event that has option to be used in debug mode or not
class DebugOutEvent(OutEvent):
    def __init__(self, debug: bool = False):
        self.debug = debug


# SqlQueryCheckEvent: Event to output a Nav source's SQL query
class SqlQueryCheckEvent(OutEvent):
    def __init__(self, source_name: str, dsn_name: str, sql_query: str):
        self.source_name = source_name
        self.dsn_name = dsn_name
        self.sql_query = sql_query


# ImportEvent: Event to output imported data
class ImportEvent(OutEvent):
    def __init__(self, source_name: str, source_type: str, source_table: pd.DataFrame, export_file_name: Optional[str] = None):
        self.name = source_name
        self.source_type = source_type
        self.source_table = source_table
        self.export_file_name = export_file_name


# StepEvent: Event to output the current step being run in the report
class StepEvent(OutEvent):
    def __init__(self, step_name: str, step_no: Optional[int] = None):
        self.step_name = step_name
        self.step_no = step_no


# TableCheckEvent: Event to check the look of a certain table
class TableCheckEvent(DebugOutEvent):
    def __init__(self, table_name: str, source_table: pd.DataFrame, export_file_name: Optional[str] = None, debug: bool = False):
        super().__init__(debug)
        self.name = table_name
        self.source_table = source_table
        self.export_file_name = export_file_name


# PrintEvent: Event to print out text
class PrintEvent(DebugOutEvent):
    def __init__(self, text: str, debug: bool = False, end_with_new_line: bool = True):
        super().__init__(debug)
        self.text = text
        self.end_with_new_line = end_with_new_line


# ListPrintEvent: Event to print out a list
class ListPrintEvent(DebugOutEvent):
    def __init__(self, lst: List[Any], flatten: bool = False, debug: bool = False, prefix: Optional[str] = None, suffix: Optional[str] = None):
        super().__init__(debug)
        self.lst = lst
        self.flatten = flatten
        self.prefix = prefix
        self.suffix = suffix


# ErrEvent: Event to print when there is an error
class ErrEvent(DebugOutEvent):
    def __init__(self, exception: BaseException, no_decorator: bool = False, debug: bool = False):
        super().__init__()
        self.exception = exception
        self.no_decorator = no_decorator
        self.debug = debug
