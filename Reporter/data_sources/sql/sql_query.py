import enum
from .logical import And, Or, Not, Comma, Operator
from .sql_join import SqlJoin
from typing import List, Union, Optional


SQL_ALL = "*"


# SqlActionType: Types of functions for an sql query
class SqlActionType(enum.Enum):
    Select = "SELECT"
    Insert = "INSERT"
    Delete = "DELETE"
    Update = "UPDATE"


# SqlQuery: Class to parse an sql query
class SqlQuery():
    def __init__(self, action: SqlActionType, selection: Union[str, List[str]], location: str, join: List[Union[str, SqlJoin]] = [], condition: Optional[Union[str, Operator]] = None):
        self.action = action
        self.selection = selection
        self.location = location
        self.join = join
        self.condition = condition


    # parse(): Parses the sql query to be used
    def parse(self):
        result = ""

        # retrieve the selection
        selection = self.selection
        if (isinstance(self.selection, List)):
            selection = Comma(self.selection).parse_sql()

        # retrieve the join needed
        join = ""
        if (self.join):
            for j in self.join:
                if (isinstance(j, SqlJoin)):
                    join += f"\n{j.parse()}"

        # retrieve the condition needed
        condition = self.condition
        if (isinstance(self.condition, Operator)):
            condition = self.condition.parse_sql()

        if (condition is not None):
            condition = f"\nWHERE {condition}"
        else:
            condition = ""

        if (self.action == SqlActionType.Select):
            result += f"{self.action.value} {selection}\nFROM {self.location}{join}{condition};"

        return result
