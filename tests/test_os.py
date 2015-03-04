
from unittest import TestCase
from cloudtb.os import split
import os


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
