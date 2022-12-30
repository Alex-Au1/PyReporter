## Quickstart

#### Writing a table to a sheet in an Excel file

```python
import pandas as pd
import Reporter as rp

view = rp.ReportSubject()
view.attach(rp.ExcelObserver())

data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

view.notify(rp.ExcelExportEvent({"First Sheet": [rp.ExcelDf(data)]}, "output.xlsx"))
```

## More Examples

#### Writing multiple tables onto the same sheet in an Excel file

```python
import pandas as pd
import Reporter as rp

view = rp.ReportSubject()
view.attach(rp.ExcelObserver())


data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
data2 = pd.DataFrame({"a": ["cell 1", "cell 2"], "b": ["cell 3", "cell 4"]})

tbl2_row = 4
tbl2_col = 3

# output 4 tables onto the same sheet, each table seperated by one cell of space
view.notify(rp.ExcelExportEvent({"First Sheet": [rp.ExcelDf(data),
                                                 rp.ExcelDf(data2, startrow = tbl2_row),
                                                 rp.ExcelDf(data, startcol = tbl2_col),
                                                 rp.ExcelDf(data2, startrow = tbl2_row, startcol = tbl2_col)]}, "output.xlsx"))
```
