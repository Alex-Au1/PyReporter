from typing import Any, Optional


# Cell: Object for each cell in a dataframe
class Cell():
    def __init__(self, value: Any, excel_formula: Optional[str] = None):
        self.value = value
        self.excel_formula = excel_formula


    def __str__(self) -> str:
        return str(self.value)


    def __mul__(self, other: Any):
        return self.value * other


    def __rmul__(self, other: Any):
        return other * self.value


    # get_display(): Retrieves the value to be displayed
    def get_display(self) -> Any:
        if (self.excel_formula is None):
            return self.value
        else:
            return self.excel_formula
