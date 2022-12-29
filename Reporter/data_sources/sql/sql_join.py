import enum
from .logical import And, Or, Not, Comma, Operator
from typing import List, Union, Optional


# SqlJoinType: Types of joining
class SqlJoinType(enum.Enum):
    InnerJoin = "INNER JOIN"
    LeftOuterJoin = "LEFT JOIN"
    RightOuterJoin = "RIGHT JOIN"
    OuterJoin = "FULL OUTER JOIN"


# SqlJoin: Class to deal with joining in sql
class SqlJoin():
    def __init__(self, join_type: SqlJoinType, table: str, condition: Union[str, Operator]):
        self.join_type = join_type
        self.table = table
        self.condition = condition

    # parse(): Parses the string representation of the join query
    def parse(self) -> str:
        condition = self.condition
        if (isinstance(self.condition, Operator)):
            condition = self.condition.parse_sql()

        return f"{self.join_type.value} {self.table} ON {condition}"
