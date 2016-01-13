from enum import Enum
from copy import copy, deepcopy
import unittest

from cloudtb.collections import (AttrDict, SolidDict, TypedDict,
                                 TypedEnum, TypedList)

mystr = 'abcdefg'
mydict = dict(zip(mystr, range(len(mystr))))
mydict['own'] = copy(mydict)


class abc(Enum):
    a = 0
    b = 1
    c = 2


class TestAttrDict(unittest.TestCase):
    def test_basic(self):
        attrdict = AttrDict(mydict)
        assert copy(attrdict) is not attrdict
        assert copy(attrdict) == attrdict
        assert deepcopy(attrdict) == attrdict
        assert isinstance(attrdict['own'], AttrDict)

    def test_descriptor(self):
        '''Tests the descriptor feature of the attr dict'''
        enum = TypedEnum(abc)
        attr = AttrDict(enum=enum, a=2)
        attr.a = 3
        assert attr['a'] == 3
        attr.enum = 0
        assert attr.enum == 'a'

    def test_set_update(self):
        '''Makes sure that object can set values like "update" that are
        also attributes (through item assignment)'''
        attrdict = AttrDict(mydict)
        attrdict['update'] = 'hi'
        self.assertNotEqual(attrdict.update, attrdict['update'])
        self.assertEqual(attrdict['update'], 'hi')

    def test_drop_unknown(self):
        pass  # TODO


class TestSolid(unittest.TestCase):
    def test_basic(self):
        solid = SolidDict(mydict)
        assert isinstance(solid['own'], SolidDict)
        solid.f = 8
        assert solid.f is 8
        assert solid['f'] == solid.f
        self.assertRaises(AttributeError, setattr, solid, 'dne', 'whatever')


class TestTypedDict(unittest.TestCase):
    def test_set(self):
        convert = TypedDict(mydict)
        convert.a = 8  # works
        assert convert.a == 8
        convert['b'] = 9.3  # works
        assert convert['b'] == 9
        assert convert.b == convert['b']

    def test_error(self):
        # import ipdb; ipdb.set_trace()
        convert = TypedDict(mydict)
        self.assertRaises(ValueError, setattr, convert, 'c', 'hello')

    def test_set_update(self):
        '''Makes sure that object can set values like "update" that are
        also attributes (through item assignment)'''
        udict = deepcopy(mydict)
        udict['update'] = 'start'
        attrdict = TypedDict(udict)
        self.assertEqual(attrdict['update'], 'start')
        attrdict['update'] = 'hi'
        self.assertNotEqual(attrdict.update, 'hi')
        self.assertEqual(attrdict['update'], 'hi')
        attrdict.update({
            'update': 'hello'
        })
        self.assertNotEqual(attrdict.update, 'hello')
        self.assertEqual(attrdict['update'], 'hello')

    def test_readonly(self):
        frozen = TypedDict(mydict)
        frozen.readonly = True
        self.assertRaises(TypeError, setattr, frozen, 'a', 5)
        self.assertRaises(TypeError, setattr, frozen, 'own', TypedDict({}))
        self.assertRaises(TypeError, setattr, frozen, 'own', {})

    def test_descriptor(self):
        venum = TypedEnum(abc)
        data = dict(mydict)
        data['enum'] = venum
        data = TypedDict(data)
        data.enum = 1
        self.assertEqual(data.enum, 'b')
        self.assertRaises(ValueError, data.__setattr__, 'enum', 'z')


class TestTypedList(unittest.TestCase):
    def test_append(self):
        mylist = list(range(10))
        l = TypedList(int, mylist)
        assert l == mylist
        l.append(10)
        l.append(13.4)
        l.append('67')
        assert l[-3:] == [10, 13, 67]

    def test_drop_unknown(self):
        pass  # TODO

    def test_type_error(self):
        mylist = list(range(10))
        l = TypedList(int, mylist)
        self.assertRaises(ValueError, l.append, 'hello')
        self.assertRaises(ValueError, l.__setitem__, 5, 'hello')

    def test_setitem(self):
        mylist = list(range(10))
        l = TypedList(int, mylist)
        l[0] = 100
        assert l[0] == 100
        l[1] = 3.23423
        assert l[1] == 3


class TestTypedEnum(unittest.TestCase):
    def test_value_enum_only(self):
        venum = TypedEnum(abc)
        venum.value = 'a'
        venum.value = 1
        venum.value = abc.a
        with self.assertRaises(ValueError):
            venum.value = 6

    def test_setting(self):
        venum = TypedEnum(abc)
        venum.value = 1
        self.assertEqual(venum.name, 'b')

    def test_descriptor(self):
        venum = TypedEnum(abc)
        venum.__set__(None, 1)
        self.assertEqual(venum.__get__(None, None), 'b')

    def test_setting_enum(self):
        '''enum should be able to be set with another enum object'''
        venum = TypedEnum(abc)
        venum2 = TypedEnum(abc)
        venum2.__set__(None, 'b')
        venum.__set__(None, venum2)
        self.assertEqual(venum.value, venum2.value)
        self.assertEqual(venum.value, 1)
