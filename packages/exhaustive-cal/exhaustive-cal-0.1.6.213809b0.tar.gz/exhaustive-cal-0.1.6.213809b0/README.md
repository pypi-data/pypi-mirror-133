# exhaustive-cal

## Usage

This package is using for exhausting every operator and calculate the expressions for objects.

## How to use it

import it by: `from exhaucal import *`. No any additional modules or packages will be installed. If you cannot install it by pip, please download the source and extract it into sys.path.

To see examples, please type `ValueExhaustive.__doc__` after importing.

Or you can make some fun things!
```python3
>>> from exhaucal import *
>>> ValueExhaustive((1, 1, 4, 5, 1, 4), "+-*/%&|^", "+-*/%&|^", ("+", "-", "*", "/", "%", "&", "|", "^", "**"), "+-*/%&|^", "+-*/%&|^").listexpr()
('1+1+4+5+1+4', '1+1+4+5+1-4', [[36860 omitted]], '1^1^4**5^1|4', '1^1^4**5^1^4')
```
