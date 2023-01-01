## Quickstart

#### Reading a table from an Excel File

<details>
  <summary> Available Files to Read </summary>
  
  ***input.xlsx***
  
  <img width="404" alt="basic_reading_input" src="https://user-images.githubusercontent.com/45087631/210046932-e4de42f0-0377-4eb9-b660-fb0789437f14.png">
</details>

```python
import pandas as pd
import Reporter as rp
import asyncio


# reads a table from the input file
async def main():
    data_sources = rp.DataSources()
    data_sources["MyInput"] = rp.SourceManager("Random Data Source", "input method 1", {"input method 1": rp.ExcelSource("input.xlsx")})

    output = await data_sources["MyInput"].prepare()
    print(output)


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()
```


<details>
  <summary> Output Result </summary>
  
  ```
     a  b
  0  1  3
  1  2  4
  ```
</details>


## More Examples

####  Reading only a portion of a table not centered at A1


<details>
  <summary> Available Files to Read </summary>
  
  ***input2.xlsx***

  <img width="424" alt="subset_reading_input" src="https://user-images.githubusercontent.com/45087631/210122610-f021696e-019a-482b-ac6e-fd9f94a2f3c5.png">

</details>

```python
import pandas as pd
import Reporter as rp
import asyncio


async def main():
    data_sources = rp.DataSources()
    data_sources["MyInput"] = rp.SourceManager("Only Numbers", "Read Table",
                                               {"Read Table": rp.ExcelSource("input2.xlsx", post_processor = {"full set": rp.DFProcessor(header_row_pos = 1, top = 2, bottom = 7, left = 2, right = 6),
                                                                                                              "subset": rp.DFProcessor(header_row_pos = 1, top = 3, bottom = -1, left = 3, right = -1)})})

    # prints out only the numbers in the table
    output = await data_sources["MyInput"].prepare("subset")
    print(f"-- Subset --\n{output}")

    # prints the full table
    output = await data_sources["MyInput"].prepare("full set")
    print(f"\n-- Full Table --\n{output}")


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()

```

<details>
  <summary> Output Result </summary>
  
  ```
-- Subset --
1 col 2 col 3
3     1     4
4     2     5
5     3     6

-- Full Table --
1       col 1       col 2       col 3       col 4
2  don't read  don't read  don't read  don't read
3  don't read           1           4  don't read
4  don't read           2           5  don't read
5  don't read           3           6  don't read
6  don't read  don't read  don't read  don't read
  ```
</details>


#### Renaming Columns from a table in a specific sheet in Excel


<details>
  <summary> Available Files to Read </summary>
  
  ***input3.xlsx***
  
  <img width="452" alt="rename_read_input" src="https://user-images.githubusercontent.com/45087631/210123430-c7f0fb0f-94b1-4ff2-8706-970705965983.png">
</details>

```python
import pandas as pd
import Reporter as rp
import asyncio


async def main():
    data_sources = rp.DataSources()
    data_sources["MyInput"] = rp.SourceManager("Renamed Columns", "Rename",
                                               {"Rename": rp.ExcelSource("input3.xlsx", "Target Sheet",
                                                                          post_processor = rp.DFProcessor(header_row_pos = 2, top = 3, bottom = 4, left = 2, right = 7,
                                                                                                          renamed_columns = {"bad col 1": "key 1",
                                                                                                                             "bad col 3": "key 2",
                                                                                                                             "bad col 5": "key 3"},
                                                                                                          ind_renamed_columns = {1: "ind 1",
                                                                                                                                 3: "ind 2"}))})

    # renames the columns in the table
    output = await data_sources["MyInput"].prepare()
    print(output)


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()
```


<details>
  <summary> Output Result </summary>
  
  ```
  2 key 1 ind 1 key 2 ind 2 key 3
  3     a     b     c     d     e
  ```
</details>


#### Select a subset of Columns

<details>
  <summary> Available Files to Read </summary>
  
  ***input4.xlsx***
  
  <img width="539" alt="select_cols_input" src="https://user-images.githubusercontent.com/45087631/210184631-4031bf11-0665-4a79-8c54-f5bbefbf3a21.png">
</details>

```python
import pandas as pd
import Reporter as rp
import asyncio


async def main():
    data_sources = rp.DataSources()
    data_sources["MyInput"] = rp.SourceManager("Renamed Columns", "Rename",
                                               {"Rename": rp.ExcelSource("input4.xlsx",
                                                                          post_processor = {"original": rp.DFProcessor(header_row_pos = 1, top = 2, bottom = 5, left = 1, right = 7),
                                                                                            "filtered": rp.DFProcessor(header_row_pos = 1, top = 2, bottom = 5, left = 1, right = 7,
                                                                                                                       ind_selected_columns = [0, 2], selected_columns = ["select 3", "repeat"])})})
                                                                                                                       
    # select the correct columns
    output = await data_sources["MyInput"].prepare("filtered")
    print(f"-- Selected Columns --\n{output}")

    # the original table
    output  = await data_sources["MyInput"].prepare("original")
    print(f"\n-- Original Table --\n{output}")


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()

```

<details>
  <summary> Output Result </summary>
  
  ```
-- Selected Columns --
1             select 1             select 2             select 3
2                    1                    3                    5
3                    a                    c                    e
4  2019-01-20 00:00:00  2019-01-22 00:00:00  2019-01-24 00:00:00

-- Original Table --
1             select 1       don't select 1             select 2       don't select 2             select 3       don't select 3
2                    1                    2                    3                    4                    5                    6
3                    a                    b                    c                    d                    e                    f
4  2019-01-20 00:00:00  2019-01-21 00:00:00  2019-01-22 00:00:00  2019-01-23 00:00:00  2019-01-24 00:00:00  2019-01-25 00:00:00
  ```
</details>


#### Remove Duplicate Row Entries for Distinct Columns

<details>
  <summary> Available Files to Read </summary>
  
  ***input4.xlsx***
  
  <img width="455" alt="distinct_cols_input" src="https://user-images.githubusercontent.com/45087631/210185873-6f316024-9350-4e43-815d-1d1fee3a7820.png">
</details>


```python
import pandas as pd
import Reporter as rp
import asyncio


async def main():
    data_sources = rp.DataSources()
    data_sources["MyInput"] = rp.SourceManager("Distinct Columns", "no duplicate rows",
                                               {"no duplicate rows": rp.ExcelSource("input5.xlsx",
                                                                                post_processor = {"original": rp.DFProcessor(header_row_pos = 3, top = 4, bottom = 9, left = 2, right = 8),
                                                                                                  "filtered": rp.DFProcessor(header_row_pos = 3, top = 4, bottom = 9, left = 2, right = 8,
                                                                                                                             distinct_columns = ["distinct 1", "distinct 2", "distinct 3"])})})

    # table without duplicate rows for the selected distinct columns
    output = await data_sources["MyInput"].prepare("filtered")
    print(f"--  Distinct Columns --\n{output}")

    # the original table
    output  = await data_sources["MyInput"].prepare("original")
    print(f"\n-- Original Table --\n{output}")


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()

```


<details>
  <summary> Output Result </summary>
  
  ```
  --  Distinct Columns --
  3 id distinct 1 col 1 col 2 distinct 2 distinct 3
  4  1          a   aba   cdc          b          c
  6  3          d   tet   wew          e          f
  7  4          g   ete   gdg          h          i

  -- Original Table --
  3 id distinct 1 col 1 col 2 distinct 2 distinct 3
  4  1          a   aba   cdc          b          c
  5  2          a   rer   rer          b          c
  6  3          d   tet   wew          e          f
  7  4          g   ete   gdg          h          i
  8  5          d   tet   wew          e          f
  ```
</details>
