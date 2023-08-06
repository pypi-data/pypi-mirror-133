# Milwaukee, Wisconsin Department of Public Works Parser

Gets the next upcoming trash and recycling date for an address in Milwaukee, WI. 

### Installation

`pip install milwaukee-dpw-parser`

### Run

```
from milwaukee_dpw_parser import get_next_garbage_and_recycling_dates
garbage_date, recycling_date = await get_next_garbage_and_recycling_dates('1011', 'E', 'BRADY', 'ST')
print(garbage_date)
print(recycling_date)
```

```
2022-01-11
2022-01-19
```

