import re
from unittest import TestCase

from cloudtb.re import research, Group, groups


class TestGroup(TestCase):
    def test_basic(self):
        exp = '(foo).*(bar)'
        text = 'foo is the opposite of bar'
        searched = re.search(exp, text)
        grps = groups(searched)
        self.assertEqual(grps, (text, 'foo', 'bar'))
        group = Group(text, searched, grps)
        matches = group
        self.assertEqual(group.text, text)
        self.assertEqual(group.indexes, {0})
        self.assertEqual(matches[0].text, 'foo')
        self.assertEqual(matches[0].indexes, {1})
        self.assertEqual(matches[1], ' is the opposite of ')
        self.assertEqual(matches[2].text, 'bar')
        self.assertEqual(matches[2].indexes, {2})

        self.assertEqual(matches[0].index, 1)
        self.assertEqual(matches[2].index, 2)

    def test_embedded(self):
        exp = '(foo (bar)).*(foo bar)'
        text = 'foo bar is grouped differently than foo bar'
        searched = re.search(exp, text)
        grps = groups(searched)
        self.assertEqual(grps, (text, 'foo bar', 'bar', 'foo bar'))
        group = Group(text, searched, grps)
        matches = group
        self.assertEqual(matches[0].text, 'foo bar')
        self.assertEqual(matches[0].indexes, {1})
        self.assertEqual(matches[0][0], 'foo ')
        self.assertEqual(matches[0][1].text, 'bar')
        self.assertEqual(matches[0][1].indexes, {2})
        self.assertIsInstance(matches[1], str)
        self.assertEqual(matches[1], ' is grouped differently than ')
        self.assertEqual(matches[2].text, 'foo bar')
        self.assertEqual(matches[2].indexes, {3})

    def test_or(self):
        exp = r'(other)|(foo \d)|(foo 9)'
        text = 'foo 9'
        searched = re.search(exp, text)
        group = Group(text, searched, groups(searched))
        # Interestingly, re stops matching once something has been
        # matched. This makes sense, as it will improve performance
        self.assertEqual({0, 2}, group.indexes)
        self.assertEqual(2, group.index)

    def test_sub(self):
        exp = '(foo).*(bar)'
        text = 'foo is the opposite of bar'
        searched = re.search(exp, text)
        group = Group(text, searched)
        matches = group
        group.sub('zaz', 1)
        self.assertEqual('zaz', matches[0].replaced)

    def test_sub_embedded(self):
        exp = '(foo (bar)).*(foo bar)'
        text = 'foo bar is grouped differently than foo bar'
        searched = re.search(exp, text)
        group = Group(text, searched)
        matches = group
        group.sub('zaz', 2)
        self.assertEqual('zaz', matches[0][1].replaced)
        expected = '[[foo [zaz#2]#1] is grouped differently than [foo bar#3]#0]'
        self.assertEqual(expected, str(group))

    def test_str(self):
        exp = '(foo (bar)).*(foo bar)'
        text = 'foo bar is grouped differently than foo bar'
        searched = re.search(exp, text)
        group = Group(text, searched, groups(searched))
        expected = "[[foo [bar#2]#1] is grouped differently than [foo bar#3]#0]"
        self.assertEqual(str(group), expected)


class TestResearch(TestCase):
    def test_basic(self):
        exp = '(foo).*?(bar)'
        text = 'so foo is the opposite of bar but without foo there is no bar?'
        searched = research(exp, text)
        self.assertEqual(searched[0], 'so ')
        self.assertEqual(searched[1].text, 'foo is the opposite of bar')
        self.assertEqual(searched[2], ' but without ')
        self.assertEqual(searched[3].text, 'foo there is no bar')
        self.assertEqual(searched[4], '?')

        matches = searched.matches
        self.assertEqual(2, len(matches))
        self.assertEqual('foo is the opposite of bar', matches[0].text)

    def test_str(self):
        exp = '(foo).*(bar)'
        text = 'so foo is the opposite of bar but without foo there is no bar?'
        searched = research(exp, text)
        expected = ('so [[foo#1] is the opposite of bar but without foo there '
                    'is no [bar#2]#0]?')
        self.assertEqual(str(searched), expected)
