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

