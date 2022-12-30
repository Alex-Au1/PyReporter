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
