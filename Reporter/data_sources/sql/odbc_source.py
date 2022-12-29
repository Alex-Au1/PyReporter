import pyodbc
import pandas as pd
from .sql_query import SqlQuery
from typing import Callable, Any, Union


# ODBC: Wrapper to deal with ODBC connections
class ODBC():
    def __init__(self, dsn_name: str):
        self.dsn = dsn_name
        self.conn = None


    # connect(): Connects to the server
    def connect(self):
        self.conn = pyodbc.connect(f"DSN={self.dsn}")
        self.cursor = self.conn.cursor()


    # check_connect(func): Decorator to check if the server connection is specified
    def check_connect(func: Callable[..., Any]):
        def check_connect_helper(self, *args, **kwargs) -> Any:
            if (self.conn is not None):
                return func(self, *args, **kwargs)

        return check_connect_helper


    # execute(query): Executes sql queries to the server
    @check_connect
    def execute(self, query: Union[str, SqlQuery]) -> pyodbc.Cursor:
        sql_query = query
        if (isinstance(query, SqlQuery)):
            sql_query = query.parse()

        self.cursor.execute(sql_query)
        return self.cursor
