from unittest import TestCase
from cloudtb import builtin


class TestStrBytes(TestCase):
    def test_encode(self):
        mystr = 'hello I am a string'
        self.assertEqual(builtin.decode(mystr), mystr)
        self.assertEqual(builtin.encode(mystr), b'hello I am a string')

    def test_decode(self):
        mybytes = b'hello I am some bytes'
        self.assertEqual(builtin.encode(mybytes), mybytes)
        self.assertEqual(builtin.decode(mybytes), 'hello I am some bytes')


class TestIsIter(TestCase):
    def test_simple(self):
        isiter = builtin.isiter
        assert isiter(tuple())
        assert isiter(list())
        assert not isiter('hi')
        assert isiter(iter(list()))


class TestEnum(TestCase):
    def test_create(self):
        try:
            from enum import Enum
        except ImportError:
            return
        class abc(Enum):
            a = 0
            b = 1
            c = 2
        myabc = builtin.enum(dict(a=0, b=1, c=2))

        def todict(e):
            return {i.name: i.value for i in e}

        self.assertEqual(todict(abc), todict(myabc))


class TestDuplicates(TestCase):
    def test_baisc(self):
        data = [1, 1, 5, 2, 6, 6, 8, 1, 5]
        expected = [1, 2, 5, 6, 8]
        result = builtin.remove_duplicates(data)
        assert result == expected

