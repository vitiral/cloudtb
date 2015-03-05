# Cloud Toolbox (cloudtb)

This library contains various convinience functions that can be used for 
common problems in python.  The unit tests work in both python 2 and 3
and continued support is intended

**For bugs and other issues** see the [github page]
(https://github.com/cloudformdesign/cloudtb)

Each library is named according to the library/function they are targeting. 
Most of these modules target distributions of scientific python and data analysis

The cloudtb should be used something like:
```
from cloudtb.pandas import dataframe_dict
# or
import cloudtb as tb
tb.pandas  # ... do something
```

it is a bad idea to do:
```
from cloudtb import pandas
```
as this could cause confusion with the actual pandas library


## Module Overview
### builtin
Tons of useful functions for a whole range of different applications. 
Everything from `isiter` to `throw` and `raises`

### re
Helpful library for working with regular expressions. Especially useful for 
experiementation and repeated searching.
```
text = 'so foo is the opposite of bar but without foo there is no bar?'
exp = '(foo).*?(bar)'
searched = cre.research(exp, text)
print(searched)
```
![re formatted](http://i.imgur.com/8baPoCY.png)
- repr of regular expression is formated: `[]` are around all matches, and their group number is marked with `#`
- Output is colorized. Matches are in magenta, their group number and formatting are in cyan
- `searched.matches` gives only the matched objects, otherwise `searched` is just a tuple of raw strings and `Group` objects
- Check out the documentation for more details
