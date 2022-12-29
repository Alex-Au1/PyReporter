from typing import List, Union


# Operator: class for an operator for sql
# Requires: 'params' is either:
#               - str
#               - Operator
class Operator():
    def __init__(self, params):
        self.params = params


    # parse_sql: parses the logical operation to be used in sql
    def parse_sql(self) -> str:
        pass


# BinaryOP: An operator that takes in 2 or more parameters
# Requires: 'params' has 2 or more elements
class BinaryOP(Operator):
    def __init__(self, params: List[Union[Operator, str]], sql_name: str, with_brackets: bool = True):
        super().__init__(params)
        self.sql_name = sql_name
        self.with_brackets = with_brackets


    # parse_sql: parses the logical operation to be used in sql
    def parse_sql(self) -> str:
        added_op = False
        result = ""

        if (self.with_brackets):
            result += "("

        for p in self.params:
            if (added_op):
                result += f" {self.sql_name} "
            else:
                added_op = True

            if (isinstance(p, str)):
                result += p
            else:
                result += p.parse_sql()

        if (self.with_brackets):
            result += ")"
        return result


# UnaryOP: An operator that takes in 1 parameter
# Requires: 'params' has at least 1 element
class UnaryOP(Operator):
    def __init__(self, param: Union[Operator, str], sql_name: str):
        super().__init__([param])
        self.sql_name = sql_name


    # parse_sql: parses the logical operation to be used in sql
    def parse_sql(self) -> str:
        result = f"({self.sql_name} "
        target_element = self.params[0]

        if (isinstance(target_element, str)):
            result += target_element
        else:
            result += target_element.parse_sql()

        result += ")"
        return result


# And: AND operator used for sql
class And(BinaryOP):
    def __init__(self, params: List[Union[Operator, str]]):
        super().__init__(params, "AND")


# Or: Or operator used for sql
class Or(BinaryOP):
    def __init__(self, params: List[Union[Operator, str]]):
        super().__init__(params, "OR")


# Not: Not operator used for sql
class Not(UnaryOP):
    def __init__(self, params: List[Union[Operator, str]]):
        super().__init__(params, "NOT")


# Comma: Used for list of items in sql
class Comma(BinaryOP):
    def __init__(self, params: List[str]):
        super().__init__(params, ",", with_brackets = False)
