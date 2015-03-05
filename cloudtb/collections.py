# -*- coding: utf-8 -*-
'''
Useful collections objects

Written in 2015 by Garrett Berg <garrett@cloudformdesign.com>

© Creative Commons 0
To the extent possible under law, the author(s) have dedicated all copyright
and related and neighboring rights to this software to the public domain
worldwide. THIS SOFTWARE IS DISTRIBUTED WITHOUT ANY WARRANTY.
<http://creativecommons.org/publicdomain/zero/1.0/>
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import sys
from copy import deepcopy
from six import reraise, iteritems, iterkeys


class AttrDict(dict):
    '''Dictionary that allows item access via getattr
    It also does some fun stuff with descriptors to allow objects in
    it's dictionary to use descriptors (you can define the
    __get__ and __set__ methods of items and they will be used)

    Developer Notes:
    -   This object is designed so that ALL user attributes go into the
        dictionary. Think if it as:
            attrdict.key = value := attrdict['key'] = value
    -   This upholds descriptors for lesser objects, to make for default
            item assignment and typing
    '''
    readonly = False  # doesn't allow item setting at all

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        # Make all internal dictionaries be own type. Make sure this
        # Overrides any super class's settings
        for key, value in iteritems(self):
            if type(value) == dict:
                dict.__setitem__(self, key, self.__class__(value))

    def update(self, value, drop_unknown=False, drop_logger=None):
        '''Update self from a value dictionary.

        If values have their own `update` methods defined, values
        are passed onto them. This allows values to choose how
        they are updated and preserves pointers
        '''
        if isinstance(value, dict):
            value = iteritems(value)
        if drop_unknown:
            newv = {}
            for key, value in value:
                if key in self:
                    newv[key] = value
                else:
                    if drop_logger is not None:
                        drop_logger(key)
            value = iteritems(newv)
        for key, value in value:
            if hasattr(self[key], 'update'):
                try:
                    self[key].update(value, drop_unknown=drop_unknown,
                                            drop_logger=drop_logger)
                except TypeError:
                    self[key].update(value)
            else:
                self[key] = value

    def _get_attr(self, attr):
        '''Bypass the special functionality of this class.

        Convience function to bypass the special __getattribute__
        funcitonality (specifically descriptors in items)
        '''
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            return self._get_item(attr)

    def _get_item(self, item):
        '''Bypass the specfial functionality of this class.

        Convinience function to pypass special machinery
        (like descriptors in items)
        '''
        return dict.__getitem__(self, item)

    def _get(self, obj):
        '''Uses descriptors where possible

        Internal function to make sure all gotten objects are treated
        the same.
        '''
        if hasattr(obj, '__get__'):
            return obj.__get__(self)
        else:
            return obj

    def _set(self, key, value):
        '''Automatically convert dictionaries set into AttrDict'''
        if isinstance(value, dict):
            value = self.__class__(value)
            assert isinstance(value, AttrDict)
        if self.readonly:
            raise TypeError('{} is read only'.format(self))
        dict.__setitem__(self, key, value)

    def __getattribute__(self, attr, keyonly=False):
        '''Where all the magic happens.

        Allows for item assignment through attribute notation and makes sure
        that object's descriptors are used
        '''
        try:
            if keyonly: raise AttributeError
            # First try the standard attr lookup and return that
            return object.__getattribute__(self, attr)
        except AttributeError:
            # all attributes that the user sets are stored in the dictionary
            # internal keys
            try:
                obj = dict.__getitem__(self, attr)
            except KeyError:
                raise AttributeError
        return self._get(obj)

    def __setattr__(self, attr, value, keyonly=False):
        '''Overrides standard setattr to allow dictionary item assignment

        Also makes sure descriptors are handled correctly.

        Dev:
            - keyonly only looks inside the dictionary keys (not attributes)
        '''
        try:
            if keyonly:
                raise AttributeError  # jump to lookup by key
            # make sure the attribute exists before we set it
            obj = object.__getattribute__(self, attr)
            # actual attr setting does NOT use special features
            #   (i.e. descriptors)
            object.__setattr__(self, attr, value)
            return
        except AttributeError:
            if attr in self:
                obj = dict.__getitem__(self, attr)
            else:  # New object, only minor checking
                return self._set(attr, value)

        if hasattr(obj, '__set__'):
            # If it is a descriptor object, let it handle everything else
            obj.__set__(self, value)
        else:
            self._set(attr, value)

    def __setitem__(self, key, value):
        self.__setattr__(key, value, keyonly=True)

    def __getitem__(self, key):
        try:
            return self.__getattribute__(key, keyonly=True)
        except AttributeError as exc:
            exc = sys.exc_info()[1:]
            reraise(KeyError, *exc)

    def __copy__(self, *args, **kwargs):
        # necessary because of recursive errors
        return self.__class__(self)

    def __deepcopy__(self, *args, **kwargs):
        # necessary because of recursive errors
        return self.__class__({key: deepcopy(value) for (key, value)
                               in iteritems(self)})

    def __basic__(self):
        '''returns self in only basic python types.

        *Should* be used for libraries like json'''
        out = {}
        for key in iterkeys(self):
            value = dict.__getitem__(self, key)
            if hasattr(value, '__basic__'):
                value = value.__basic__()
            elif hasattr(value, '__get__'):
                value = value.__get__(self, self.__class__)
            out[key] = value
        return out


class SolidDict(AttrDict):
    '''Dictionary like object that doesn't allow it's shape to change
    (cannot add or remove keys)
    Does the same for all items inside of it'''
    def __setitem__(self, item, value):
        if item not in self:
            raise KeyError(item)
        AttrDict.__setitem__(self, item, value)

    def __setattr__(self, attr, value, *args, **kwargs):
        if not hasattr(self, attr):
            raise AttributeError(attr)
        AttrDict.__setattr__(self, attr, value, *args, **kwargs)


class TypedDict(AttrDict):
    '''Dictionary like object that keeps track of types. Choose whether
    to attempt to convert types (default) or not allow different types.

    Keyword arguments:
        convert -- whether to attempt to convert values that don't match
    '''
    def __init__(self, *args, **kwargs):
        convert = kwargs.get('convert', True)
        object.__setattr__(self, '_convert', convert)
        AttrDict.__init__(self, *args, **kwargs)

    def _convert_value(self, value, curval):
        '''Convert value to type(curvalue). Also do associated error checking'''
        curtype = type(curval)
        if not isinstance(value, curtype):
            if self._convert:
                value = curtype(value)
            else:
                raise TypeError("{} is not type {}".format(value, curtype))
        return value

    def __setitem__(self, item, value):
        '''Do type conversions automatically.
        If current value is a descriptor, allow it to handle everything
        '''
        self.__setattr__(item, value, keyonly=True)

    def __setattr__(self, attr, value, keyonly=False):
        if keyonly:
            actual = self._get_item(attr)
        else:
            actual = self._get_attr(attr)
        if hasattr(actual, '__set__'):
            actual.__set__(None, value)
            return
        value = self._convert_value(value, actual)
        AttrDict.__setattr__(self, attr, value, keyonly)

    def __set__(self, obj, value):
        raise TypeError("TypedDict is a protected member")


class TypedList(list):
    '''A list that preserves types

    Arguments:
        type -- the type of list elements to preserve

    Key Word Arguments:
        convert -- whether to attempt automatic conversion to type
        noset -- don't allow setting of existing elements
    '''
    def __init__(self, type, *args, **kwargs):
        self._type = type
        self._convert = kwargs.get('convert', True)
        self._noset = kwargs.get('noset', False)
        list.__init__(self)  # make self an empty list
        self.extend(tuple(*args, **kwargs),
                    drop_unknown=kwargs.get('drop_unknown', False),
                    drop_logger=kwargs.get('drop_logger', None))

    def __basic__(self):
        '''returns self in only basic python types.'''
        out = []
        for value in list.__iter__(self):
            if hasattr(value, '__basic__'):
                value = value.__basic__()
            elif hasattr(value, '__get__'):
                value = value.__get__(self, self.__class__)
            out.append(value)
        return out

    def update(self, value, **kwargs):
        new = TypedList(self._type, value, **kwargs)  # check types
        self.clear()
        self.extend(new, **kwargs)

    def _convert_value(self, value, **kwargs):
        '''Automatic type conversion. Uses update if it exists'''
        if hasattr(self._type, 'update'):
            # Copy our type (think of it is a template)
            _type = deepcopy(self._type)
            # update the values. Values not included will remain as the default
            try:
                _type.update(value, **kwargs)
            except TypeError:
                _type.update(value)
            value = _type
        elif not isinstance(value, type):
            return self._type(value)
        return value

    def append(self, value, **kwargs):
        '''Append a value. It is type checked first'''
        value = self._convert_value(value, **kwargs)
        list.append(self, value)

    def extend(self, iterator, **kwargs):
        '''Extend self from an iterator, type checking every value'''
        for i in iterator:
            self.append(i, **kwargs)

    def __setitem__(self, item, value):
        if self._noset:
            raise IndexError("items cannot be set with noset=True")
        value = self._convert_value(value)
        list.__setitem__(self, item, value)

    def __set__(self, obj, value):
        raise TypeError("Typed List is a protected member")


class TypedEnum(object):
    '''Class to make setting of enum types valid and error checked

    This class can be put in a Typed object. It allows you to reduce
    the values that an attribute can be set to to only the values that
    are in the enum. Other values will have ValueError raised on them

    When setting, TypedEnum will first look in the enum itself, it will
    then look in the enum names, and finally it will look in the enum values.
    So if you have overlap, it will choose the name

    When getting, TypedEnun always returns the associated Enum's name

    See the unit tests for more examples
    '''
    def __init__(self, enum, default=None):
        self._enum = enum
        self._enum_by_value = {e.value: e for e in enum}
        self._enum_by_name = {e.name: e for e in enum}
        self._enum_dict = {e.name: e.value for e in enum}
        self._value = next(iter(enum))
        if default is not None:
            self.value = default

    @property
    def value(self):
        return self._value.value

    @value.setter
    def value(self, value):
        if value in self._enum:
            value = getattr(self._enum, value.name)
        elif value in self._enum_by_name:
            value = self._enum_by_name[value]
        elif value in self._enum_by_value:
            value = self._enum_by_value[value]
        else:
            raise ValueError("Value does not exist in enum: {}".format(value))
        self._value = value

    @property
    def name(self):
        return self._value.name

    def __repr__(self):
        return "Enum(value={}, possible={})".format(self._value.name,
                                                    self._enum_dict)

    def __get__(self, obj, type=None):
        return self._value.name

    def __set__(self, obj, value):
        if hasattr(value, '__get__'):
            value = value.__get__(None, None)
        self.value = value
