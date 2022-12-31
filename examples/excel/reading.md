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
