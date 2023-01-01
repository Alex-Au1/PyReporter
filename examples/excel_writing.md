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

<details>
  <summary> Output Result</summary>
  
  <img width="541" alt="basic_writing_output" src="https://user-images.githubusercontent.com/45087631/210029616-34df0cc4-f046-4214-a102-5ce3ef81179f.png">
</details>


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

<details>
  <summary> Output Result</summary>
  
  <img width="412" alt="multi_writing_output" src="https://user-images.githubusercontent.com/45087631/210029837-1964dcea-44e2-4806-9394-b1224c67bf88.png">
</details>

#### Writing tables to different sheets in an Excel file

```python
import pandas as pd
import Reporter as rp

view = rp.ReportSubject()

view.attach(rp.ExcelObserver())


data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
data2 = pd.DataFrame({"a": ["cell 1", "cell 2"], "b": ["cell 3", "cell 4"]})
data3 = pd.DataFrame({"catalan": [1, 1, 2, 5, 14, 42, 132]})


# output the number of tables indicated by the sheet name
view.notify(rp.ExcelExportEvent({"Sheet With 1 Table": [rp.ExcelDf(data)],
                                 "Sheet With 2 Tables": [rp.ExcelDf(data), rp.ExcelDf(data2, startcol = 3)],
                                 "Sheet With 3 Tables": [rp.ExcelDf(data), rp.ExcelDf(data2, startcol = 3), rp.ExcelDf(data3, startcol = 6)]} ,"output.xlsx"))

```

<details>
  <summary> Output Result</summary>
    <img width="430" alt="multi_writing2_output1" src="https://user-images.githubusercontent.com/45087631/210030283-c115bd90-d275-434d-bebf-0c8b0df8dc0f.png">
    <img width="419" alt="multi_writing2_output2" src="https://user-images.githubusercontent.com/45087631/210030881-95b756d0-d724-494b-9bdf-50c2acd6b8e2.png">
    <img width="416" alt="multi_writing2_output3" src="https://user-images.githubusercontent.com/45087631/210030885-3e9edebf-a755-49a2-b5e4-bb05d2a5d244.png">

</details>
