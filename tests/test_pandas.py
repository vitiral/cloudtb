from unittest import TestCase
from pandas.util.testing import assert_frame_equal
from cloudtb.pandas import dataframe_dict
from cloudtb.dictionary import get_header, unpack, flatten, fill_keys

strings = 'abcdefg'
testdata = {key: value for (key, value) in zip(strings, range(len(strings)))}
testdata['many'] = dict(testdata)

testdata = [testdata for n in range(10)]


class TestLoad(TestCase):
    def test_list(self):
        dataframe_dict(testdata)

    def test_dict(self):
        header = get_header(testdata[0])
        custom_data = fill_keys(flatten(unpack(testdata, header)), '')
        result = dataframe_dict(testdata)
        expected = dataframe_dict(custom_data)
        assert_frame_equal(result, expected, check_names=True)
