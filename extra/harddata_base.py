#!/usr/bin/python
# -*- coding: utf-8 -*-
#    The MIT License (MIT)
#    
#    Copyright (c) 2013 Garrett Berg cloudformdesign.com
#    An updated version of this file can be found at:
#    https://github.com/cloudformdesign/cloudtb
#    
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#    THE SOFTWARE.
#
#    http://opensource.org/licenses/MIT

    def _Printer__data(self, *args, **kwargs):
        print "_Printer__data: ", args, kwargs
        return self._get_harddata()._Printer__data(*args, **kwargs)

    def _Printer__dirs(self, *args, **kwargs):
        print "_Printer__dirs: ", args, kwargs
        return self._get_harddata()._Printer__dirs(*args, **kwargs)

    def _Printer__files(self, *args, **kwargs):
        print "_Printer__files: ", args, kwargs
        return self._get_harddata()._Printer__files(*args, **kwargs)

    def _Printer__lines(self, *args, **kwargs):
        print "_Printer__lines: ", args, kwargs
        return self._get_harddata()._Printer__lines(*args, **kwargs)

    def _Printer__name(self, *args, **kwargs):
        print "_Printer__name: ", args, kwargs
        return self._get_harddata()._Printer__name(*args, **kwargs)

    def _Printer__setup(self, *args, **kwargs):
        print "_Printer__setup: ", args, kwargs
        return self._get_harddata()._Printer__setup(*args, **kwargs)

    def __abs__(self, *args, **kwargs):
        print "__abs__: ", args, kwargs
        return self._get_harddata().__abs__(*args, **kwargs)

    def __abstractmethods__(self, *args, **kwargs):
        print "__abstractmethods__: ", args, kwargs
        return self._get_harddata().__abstractmethods__(*args, **kwargs)

    def __add__(self, *args, **kwargs):
        print "__add__: ", args, kwargs
        return self._get_harddata().__add__(*args, **kwargs)

    def __alloc__(self, *args, **kwargs):
        print "__alloc__: ", args, kwargs
        return self._get_harddata().__alloc__(*args, **kwargs)

    def __and__(self, *args, **kwargs):
        print "__and__: ", args, kwargs
        return self._get_harddata().__and__(*args, **kwargs)

    def __base__(self, *args, **kwargs):
        print "__base__: ", args, kwargs
        return self._get_harddata().__base__(*args, **kwargs)

    def __bases__(self, *args, **kwargs):
        print "__bases__: ", args, kwargs
        return self._get_harddata().__bases__(*args, **kwargs)

    def __basicsize__(self, *args, **kwargs):
        print "__basicsize__: ", args, kwargs
        return self._get_harddata().__basicsize__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        print "__call__: ", args, kwargs
        return self._get_harddata().__call__(*args, **kwargs)

    def __class__(self, *args, **kwargs):
        print "__class__: ", args, kwargs
        return self._get_harddata().__class__(*args, **kwargs)

    def __closure__(self, *args, **kwargs):
        print "__closure__: ", args, kwargs
        return self._get_harddata().__closure__(*args, **kwargs)

    def __cmp__(self, *args, **kwargs):
        print "__cmp__: ", args, kwargs
        return self._get_harddata().__cmp__(*args, **kwargs)

    def __code__(self, *args, **kwargs):
        print "__code__: ", args, kwargs
        return self._get_harddata().__code__(*args, **kwargs)

    def __coerce__(self, *args, **kwargs):
        print "__coerce__: ", args, kwargs
        return self._get_harddata().__coerce__(*args, **kwargs)

    def __contains__(self, *args, **kwargs):
        print "__contains__: ", args, kwargs
        return self._get_harddata().__contains__(*args, **kwargs)

    def __defaults__(self, *args, **kwargs):
        print "__defaults__: ", args, kwargs
        return self._get_harddata().__defaults__(*args, **kwargs)

    def __delattr__(self, *args, **kwargs):
        print "__delattr__: ", args, kwargs
        return self._get_harddata().__delattr__(*args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        print "__delitem__: ", args, kwargs
        return self._get_harddata().__delitem__(*args, **kwargs)

    def __delslice__(self, *args, **kwargs):
        print "__delslice__: ", args, kwargs
        return self._get_harddata().__delslice__(*args, **kwargs)

    def __dict__(self, *args, **kwargs):
        print "__dict__: ", args, kwargs
        return self._get_harddata().__dict__(*args, **kwargs)

    def __dictoffset__(self, *args, **kwargs):
        print "__dictoffset__: ", args, kwargs
        return self._get_harddata().__dictoffset__(*args, **kwargs)

    def __div__(self, *args, **kwargs):
        print "__div__: ", args, kwargs
        return self._get_harddata().__div__(*args, **kwargs)

    def __divmod__(self, *args, **kwargs):
        print "__divmod__: ", args, kwargs
        return self._get_harddata().__divmod__(*args, **kwargs)

    def __enter__(self, *args, **kwargs):
        print "__enter__: ", args, kwargs
        return self._get_harddata().__enter__(*args, **kwargs)

    def __eq__(self, *args, **kwargs):
        print "__eq__: ", args, kwargs
        return self._get_harddata().__eq__(*args, **kwargs)

    def __exit__(self, *args, **kwargs):
        print "__exit__: ", args, kwargs
        return self._get_harddata().__exit__(*args, **kwargs)

    def __flags__(self, *args, **kwargs):
        print "__flags__: ", args, kwargs
        return self._get_harddata().__flags__(*args, **kwargs)

    def __float__(self, *args, **kwargs):
        print "__float__: ", args, kwargs
        return self._get_harddata().__float__(*args, **kwargs)

    def __floordiv__(self, *args, **kwargs):
        print "__floordiv__: ", args, kwargs
        return self._get_harddata().__floordiv__(*args, **kwargs)

    def __format__(self, *args, **kwargs):
        print "__format__: ", args, kwargs
        return self._get_harddata().__format__(*args, **kwargs)

    def __func__(self, *args, **kwargs):
        print "__func__: ", args, kwargs
        return self._get_harddata().__func__(*args, **kwargs)

    def __ge__(self, *args, **kwargs):
        print "__ge__: ", args, kwargs
        return self._get_harddata().__ge__(*args, **kwargs)

    def __get__(self, *args, **kwargs):
        print "__get__: ", args, kwargs
        return self._get_harddata().__get__(*args, **kwargs)

    def __getformat__(self, *args, **kwargs):
        print "__getformat__: ", args, kwargs
        return self._get_harddata().__getformat__(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        print "__getitem__: ", args, kwargs
        return self._get_harddata().__getitem__(*args, **kwargs)

    def __getnewargs__(self, *args, **kwargs):
        print "__getnewargs__: ", args, kwargs
        return self._get_harddata().__getnewargs__(*args, **kwargs)

    def __getslice__(self, *args, **kwargs):
        print "__getslice__: ", args, kwargs
        return self._get_harddata().__getslice__(*args, **kwargs)

    def __globals__(self, *args, **kwargs):
        print "__globals__: ", args, kwargs
        return self._get_harddata().__globals__(*args, **kwargs)

    def __gt__(self, *args, **kwargs):
        print "__gt__: ", args, kwargs
        return self._get_harddata().__gt__(*args, **kwargs)

    def __hash__(self, *args, **kwargs):
        print "__hash__: ", args, kwargs
        return self._get_harddata().__hash__(*args, **kwargs)

    def __hex__(self, *args, **kwargs):
        print "__hex__: ", args, kwargs
        return self._get_harddata().__hex__(*args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        print "__iadd__: ", args, kwargs
        return self._get_harddata().__iadd__(*args, **kwargs)

    def __iand__(self, *args, **kwargs):
        print "__iand__: ", args, kwargs
        return self._get_harddata().__iand__(*args, **kwargs)

    def __imul__(self, *args, **kwargs):
        print "__imul__: ", args, kwargs
        return self._get_harddata().__imul__(*args, **kwargs)

    def __index__(self, *args, **kwargs):
        print "__index__: ", args, kwargs
        return self._get_harddata().__index__(*args, **kwargs)

    def __instancecheck__(self, *args, **kwargs):
        print "__instancecheck__: ", args, kwargs
        return self._get_harddata().__instancecheck__(*args, **kwargs)

    def __int__(self, *args, **kwargs):
        print "__int__: ", args, kwargs
        return self._get_harddata().__int__(*args, **kwargs)

    def __invert__(self, *args, **kwargs):
        print "__invert__: ", args, kwargs
        return self._get_harddata().__invert__(*args, **kwargs)

    def __ior__(self, *args, **kwargs):
        print "__ior__: ", args, kwargs
        return self._get_harddata().__ior__(*args, **kwargs)

    def __isub__(self, *args, **kwargs):
        print "__isub__: ", args, kwargs
        return self._get_harddata().__isub__(*args, **kwargs)

    def __itemsize__(self, *args, **kwargs):
        print "__itemsize__: ", args, kwargs
        return self._get_harddata().__itemsize__(*args, **kwargs)

    def __iter__(self, *args, **kwargs):
        print "__iter__: ", args, kwargs
        return self._get_harddata().__iter__(*args, **kwargs)

    def __ixor__(self, *args, **kwargs):
        print "__ixor__: ", args, kwargs
        return self._get_harddata().__ixor__(*args, **kwargs)

    def __le__(self, *args, **kwargs):
        print "__le__: ", args, kwargs
        return self._get_harddata().__le__(*args, **kwargs)

    def __len__(self, *args, **kwargs):
        print "__len__: ", args, kwargs
        return self._get_harddata().__len__(*args, **kwargs)

    def __length_hint__(self, *args, **kwargs):
        print "__length_hint__: ", args, kwargs
        return self._get_harddata().__length_hint__(*args, **kwargs)

    def __long__(self, *args, **kwargs):
        print "__long__: ", args, kwargs
        return self._get_harddata().__long__(*args, **kwargs)

    def __lshift__(self, *args, **kwargs):
        print "__lshift__: ", args, kwargs
        return self._get_harddata().__lshift__(*args, **kwargs)

    def __lt__(self, *args, **kwargs):
        print "__lt__: ", args, kwargs
        return self._get_harddata().__lt__(*args, **kwargs)

    def __mod__(self, *args, **kwargs):
        print "__mod__: ", args, kwargs
        return self._get_harddata().__mod__(*args, **kwargs)

    def __module__(self, *args, **kwargs):
        print "__module__: ", args, kwargs
        return self._get_harddata().__module__(*args, **kwargs)

    def __mro__(self, *args, **kwargs):
        print "__mro__: ", args, kwargs
        return self._get_harddata().__mro__(*args, **kwargs)

    def __mul__(self, *args, **kwargs):
        print "__mul__: ", args, kwargs
        return self._get_harddata().__mul__(*args, **kwargs)

    def __name__(self, *args, **kwargs):
        print "__name__: ", args, kwargs
        return self._get_harddata().__name__(*args, **kwargs)

    def __ne__(self, *args, **kwargs):
        print "__ne__: ", args, kwargs
        return self._get_harddata().__ne__(*args, **kwargs)

    def __neg__(self, *args, **kwargs):
        print "__neg__: ", args, kwargs
        return self._get_harddata().__neg__(*args, **kwargs)

    def __nonzero__(self, *args, **kwargs):
        print "__nonzero__: ", args, kwargs
        return self._get_harddata().__nonzero__(*args, **kwargs)

    def __oct__(self, *args, **kwargs):
        print "__oct__: ", args, kwargs
        return self._get_harddata().__oct__(*args, **kwargs)

    def __or__(self, *args, **kwargs):
        print "__or__: ", args, kwargs
        return self._get_harddata().__or__(*args, **kwargs)

    def __pos__(self, *args, **kwargs):
        print "__pos__: ", args, kwargs
        return self._get_harddata().__pos__(*args, **kwargs)

    def __pow__(self, *args, **kwargs):
        print "__pow__: ", args, kwargs
        return self._get_harddata().__pow__(*args, **kwargs)

    def __radd__(self, *args, **kwargs):
        print "__radd__: ", args, kwargs
        return self._get_harddata().__radd__(*args, **kwargs)

    def __rand__(self, *args, **kwargs):
        print "__rand__: ", args, kwargs
        return self._get_harddata().__rand__(*args, **kwargs)

    def __rdiv__(self, *args, **kwargs):
        print "__rdiv__: ", args, kwargs
        return self._get_harddata().__rdiv__(*args, **kwargs)

    def __rdivmod__(self, *args, **kwargs):
        print "__rdivmod__: ", args, kwargs
        return self._get_harddata().__rdivmod__(*args, **kwargs)

    def __reduce__(self, *args, **kwargs):
        print "__reduce__: ", args, kwargs
        return self._get_harddata().__reduce__(*args, **kwargs)

    def __reduce_ex__(self, *args, **kwargs):
        print "__reduce_ex__: ", args, kwargs
        return self._get_harddata().__reduce_ex__(*args, **kwargs)

    def __reversed__(self, *args, **kwargs):
        print "__reversed__: ", args, kwargs
        return self._get_harddata().__reversed__(*args, **kwargs)

    def __rfloordiv__(self, *args, **kwargs):
        print "__rfloordiv__: ", args, kwargs
        return self._get_harddata().__rfloordiv__(*args, **kwargs)

    def __rlshift__(self, *args, **kwargs):
        print "__rlshift__: ", args, kwargs
        return self._get_harddata().__rlshift__(*args, **kwargs)

    def __rmod__(self, *args, **kwargs):
        print "__rmod__: ", args, kwargs
        return self._get_harddata().__rmod__(*args, **kwargs)

    def __rmul__(self, *args, **kwargs):
        print "__rmul__: ", args, kwargs
        return self._get_harddata().__rmul__(*args, **kwargs)

    def __ror__(self, *args, **kwargs):
        print "__ror__: ", args, kwargs
        return self._get_harddata().__ror__(*args, **kwargs)

    def __rpow__(self, *args, **kwargs):
        print "__rpow__: ", args, kwargs
        return self._get_harddata().__rpow__(*args, **kwargs)

    def __rrshift__(self, *args, **kwargs):
        print "__rrshift__: ", args, kwargs
        return self._get_harddata().__rrshift__(*args, **kwargs)

    def __rshift__(self, *args, **kwargs):
        print "__rshift__: ", args, kwargs
        return self._get_harddata().__rshift__(*args, **kwargs)

    def __rsub__(self, *args, **kwargs):
        print "__rsub__: ", args, kwargs
        return self._get_harddata().__rsub__(*args, **kwargs)

    def __rtruediv__(self, *args, **kwargs):
        print "__rtruediv__: ", args, kwargs
        return self._get_harddata().__rtruediv__(*args, **kwargs)

    def __rxor__(self, *args, **kwargs):
        print "__rxor__: ", args, kwargs
        return self._get_harddata().__rxor__(*args, **kwargs)

    def __self__(self, *args, **kwargs):
        print "__self__: ", args, kwargs
        return self._get_harddata().__self__(*args, **kwargs)

    def __self_class__(self, *args, **kwargs):
        print "__self_class__: ", args, kwargs
        return self._get_harddata().__self_class__(*args, **kwargs)

    def __set__(self, *args, **kwargs):
        print "__set__: ", args, kwargs
        return self._get_harddata().__set__(*args, **kwargs)

    def __setattr__(self, *args, **kwargs):
        print "__setattr__: ", args, kwargs
        return self._get_harddata().__setattr__(*args, **kwargs)

    def __setformat__(self, *args, **kwargs):
        print "__setformat__: ", args, kwargs
        return self._get_harddata().__setformat__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        print "__setitem__: ", args, kwargs
        return self._get_harddata().__setitem__(*args, **kwargs)

    def __setslice__(self, *args, **kwargs):
        print "__setslice__: ", args, kwargs
        return self._get_harddata().__setslice__(*args, **kwargs)

    def __setstate__(self, *args, **kwargs):
        print "__setstate__: ", args, kwargs
        return self._get_harddata().__setstate__(*args, **kwargs)

    def __sizeof__(self, *args, **kwargs):
        print "__sizeof__: ", args, kwargs
        return self._get_harddata().__sizeof__(*args, **kwargs)

    def __sub__(self, *args, **kwargs):
        print "__sub__: ", args, kwargs
        return self._get_harddata().__sub__(*args, **kwargs)

    def __subclasscheck__(self, *args, **kwargs):
        print "__subclasscheck__: ", args, kwargs
        return self._get_harddata().__subclasscheck__(*args, **kwargs)

    def __subclasses__(self, *args, **kwargs):
        print "__subclasses__: ", args, kwargs
        return self._get_harddata().__subclasses__(*args, **kwargs)

    def __subclasshook__(self, *args, **kwargs):
        print "__subclasshook__: ", args, kwargs
        return self._get_harddata().__subclasshook__(*args, **kwargs)

    def __thisclass__(self, *args, **kwargs):
        print "__thisclass__: ", args, kwargs
        return self._get_harddata().__thisclass__(*args, **kwargs)

    def __truediv__(self, *args, **kwargs):
        print "__truediv__: ", args, kwargs
        return self._get_harddata().__truediv__(*args, **kwargs)

    def __trunc__(self, *args, **kwargs):
        print "__trunc__: ", args, kwargs
        return self._get_harddata().__trunc__(*args, **kwargs)

    def __unicode__(self, *args, **kwargs):
        print "__unicode__: ", args, kwargs
        return self._get_harddata().__unicode__(*args, **kwargs)

    def __weakref__(self, *args, **kwargs):
        print "__weakref__: ", args, kwargs
        return self._get_harddata().__weakref__(*args, **kwargs)

    def __weakrefoffset__(self, *args, **kwargs):
        print "__weakrefoffset__: ", args, kwargs
        return self._get_harddata().__weakrefoffset__(*args, **kwargs)

    def __xor__(self, *args, **kwargs):
        print "__xor__: ", args, kwargs
        return self._get_harddata().__xor__(*args, **kwargs)