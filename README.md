# Cloud Toolbox (cloudtb)

This library contains various convinience functions that can be used for common problems in python.
Each library is named according to the library/function they are targeting. Most of these
modules target distributions of scientific python and data analysis

The cloudtb should be used something like:
```
from cloudtb.pandas import dataframe_dict
```

it is a bad idea to do:
```
from cloudtb import pandas
```
as this could cause confusion with the actual pandas library


## Module Overview
### builtin
Tons of useful functions for a whole range of different applications. Everything from `isiter` to `throw` and `raises`

### re
```
text = 'so foo is the opposite of bar but without foo there is no bar?'
exp = '(foo).*?(bar)'
searched = cre.research(exp, text)
print(searched)
```
![re formatted](http://i.imgur.com/8baPoCY.png)

