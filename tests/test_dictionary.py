from unittest import TestCase
from cloudtb import dictionary

names = 'abcdef'
basic_dict = dict(zip(names, range(len(names))))
basic_dict['self'] = dict(basic_dict)


class TestDepth(TestCase):
    def test_basic(self):
        self.assertEqual(dictionary.depth(basic_dict), 2)


class TestHeader(TestCase):
    def test_basic(self):
        header = tuple((n,) for n in names) + tuple(zip(('self',) * len(names), names))
        header2 = dictionary.get_header(basic_dict)
        header2.reverse()
        self.assertEqual(set(header), set(header2))


class TestGetItem(TestCase):
    def test_level_1(self):
        self.assertEqual(dictionary.getitem(basic_dict, ('b',)), 1)

    def test_level_2(self):
        self.assertEqual(dictionary.getitem(basic_dict, ('self', 'b')), 1)


class TestUnpack(TestCase):
    def test_basic(self):
        diclist = [basic_dict for _ in range(10)]
        checkdict = {key: list((i,) * 10) for
                     i, key in enumerate(names)}
        checkdict['self'] = dict(checkdict)
        # TODO: unpack currently uses the header, which makes sense
        # but shouldn't be the default
        unpacked = dictionary.unpack(diclist)
        self.assertDictEqual(unpacked, checkdict)
