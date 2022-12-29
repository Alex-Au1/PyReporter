from .odbc_source import ODBC


# Nav: ODBC connection to the NAV server
class Nav(ODBC):
    def __init__(self, dsn_name: str):
        super().__init__(dsn_name)
