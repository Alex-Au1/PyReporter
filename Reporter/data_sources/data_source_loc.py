import enum


# DatSourceLoc: All possible datasource locations
class DataSourceLoc(enum.Enum):
    Nav = "nav"
    Sharepoint = "sharepoint"
    Excel = "excel"
    CustomTable = "custom table"
