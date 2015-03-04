
from unittest import TestCase
from cloudtb.os import split, abspath
import os


class TestAbspath(TestCase):
    def test_nouser(self):
        '''when there is no user, the added feature has no impact'''
        plist = ['', 'foo', 'bar', 'zaz']
        expected = os.path.sep.join(plist)
        result = abspath(expected)
        self.assertEqual(expected, result)

    def test_nouser_nonroot(self):
        plist = ['foo', 'bar', 'zaz']
        path = os.path.sep.join(plist)
        expected = os.path.abspath(path)
        result = abspath(expected)
        self.assertEqual(expected, result)


class TestSplit(TestCase):
    def test_basic(self):
        expected = ['foo', 'bar', 'zaz']
        folders = os.path.sep.join(expected)
        result = split(folders)
        self.assertEqual(expected, result)

    def test_file(self):
        expected = ['zaz']
        folders = os.path.sep.join(expected)
        result = split(folders)
        self.assertEqual(expected, result)

    def test_empty(self):
        expected = []
        folders = ''
        result = split(folders)
        self.assertEqual(expected, result)

    def test_root(self):
        expected = [os.path.sep]
        folders = os.path.sep.join(expected)
        result = split(folders)
        self.assertEqual(expected, result)

    def test_root_more(self):
        expected = ['', 'foo', 'bar', 'zaz']
        folders = os.path.sep.join(expected)
        expected[0] = os.path.sep  # if it was originally, would start with '//'
        result = split(folders)
        self.assertEqual(expected, result)
