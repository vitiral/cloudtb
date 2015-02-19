from unittest import TestCase
from pandas.util.testing import assert_frame_equal
from cloudtb.pandas import dataframe_dict
from cloudtb.dictionary import get_header, unpack, flatten

strings = 'abcdefg'
testdata = {key: value for (key, value) in zip(strings, range(len(strings)))}
testdata['many'] = dict(testdata)

testdata = [testdata for n in range(10)]


class TestLoad(TestCase):
    def test_list(self):
        dataframe_dict(testdata)

    def test_dict(self):
        header = get_header(testdata[0])
        testdata_dict = flatten(unpack(testdata, header))
        df = dataframe_dict(testdata_dict)
        df2 = dataframe_dict(testdata)
        assert_frame_equal(df, df2, check_names=True)
