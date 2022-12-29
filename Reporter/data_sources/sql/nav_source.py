import pyodbc
import pandas as pd
from .nav import Nav
from ..df_processor import DFProcessor
from ..abs_source import AbsSource
from .sql_query import SqlQuery
from ...events import SqlQueryCheckEvent
from typing import Union, Optional


# NavSource: Source table from NAV SQL
# Requires: 'query' selects a table from NAV
class NavSource(AbsSource):
    def __init__(self, nav: Nav, query: Union[str, SqlQuery], post_processor: Optional[DFProcessor] = None):
        super().__init__(post_processor)
        self.nav = nav
        self.parse_query(query)


    # parse_query(): Converts the SQL query to a string
    def parse_query(self, query):
        if (isinstance(query, SqlQuery)):
            self.query= query.parse()
        else:
            self.query = query


    # import_data(): Imports the sql table
    def import_data(self) -> pd.DataFrame:
        # notifies the SQL query for the source
        self.notify(SqlQueryCheckEvent(self.name, self.nav.dsn, self.query))

        return pd.read_sql(self.query, self.nav.conn)
