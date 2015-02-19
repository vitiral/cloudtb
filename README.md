# Cloud Toolbox (cloudtb)

This library contains various convinience functions that can be used for common problems in python.
Each library is named according to the library/function they are targeting.

The cloudtb should be used something like:
```
from cloudtb.pandas import dataframe_dict
```

it is a bad idea to do:
```
from cloudtb import pandas
```
as this could cause confusion with the actual pandas library
