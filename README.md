# PyTreasuryDirect
PyTreasuryDirect is a thin wrapper on top of the [Treasury Direct Web API][1]

## To Start
PyTreasuryDirect uses the Requests Python package. To install:
```
pip install PyTreasuryDirect
```

## Example 
```python
from pytreasurydirect import TreasuryDirect

td = TreasuryDirect()
cusip = '912796CJ6'

print(td.security_info(cusip, '02/11/2014'))
# or 
print(td.security_info(cusip, datetime.date(2014, 2, 11)))
```

[1]: https://www.treasurydirect.gov/webapis/webapisindex.htm 
