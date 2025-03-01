from tests.config import error_analysis, sample_data, CORRELATION, CORRELATION_THRESHOLD, VERBOSE
from tests.context import pandas_ta

from unittest import skip, TestCase
import pandas.testing as pdt
from pandas import DataFrame, Series

import talib as tal


class TestStatistics(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.data.columns = cls.data.columns.str.lower()
        cls.open = cls.data["open"]
        cls.high = cls.data["high"]
        cls.low = cls.data["low"]
        cls.close = cls.data["close"]
        if "volume" in cls.data.columns:
            cls.volume = cls.data["volume"]

    @classmethod
    def tearDownClass(cls):
        del cls.open
        del cls.high
        del cls.low
        del cls.close
        if hasattr(cls, "volume"):
            del cls.volume
        del cls.data

    def setUp(self): pass
    def tearDown(self): pass


    def test_entropy(self):
        result = pandas_ta.entropy(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "ENTP_10")

    def test_kurtosis(self):
        result = pandas_ta.kurtosis(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "KURT_30")

    def test_mad(self):
        result = pandas_ta.mad(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "MAD_30")

    def test_median(self):
        result = pandas_ta.median(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "MEDIAN_30")

    def test_quantile(self):
        result = pandas_ta.quantile(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "QTL_30_0.5")

    def test_skew(self):
        result = pandas_ta.skew(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "SKEW_30")

    def test_stdev(self):
        result = pandas_ta.stdev(self.close, talib=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "STDEV_30")

        try:
            expected = tal.STDDEV(self.close, 30)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

        result = pandas_ta.stdev(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "STDEV_30")

    def test_tos_sdtevall(self):
        result = pandas_ta.tos_stdevall(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "TOS_STDEVALL")
        self.assertEqual(len(result.columns), 7)

        result = pandas_ta.tos_stdevall(self.close, length=30)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "TOS_STDEVALL_30")
        self.assertEqual(len(result.columns), 7)

        result = pandas_ta.tos_stdevall(self.close, length=30, stds=[1, 2])
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "TOS_STDEVALL_30")
        self.assertEqual(len(result.columns), 5)

    def test_variance(self):
        result = pandas_ta.variance(self.close, talib=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "VAR_30")

        try:
            expected = tal.VAR(self.close, 30)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

        result = pandas_ta.variance(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "VAR_30")

    def test_zscore(self):
        result = pandas_ta.zscore(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "ZS_30")
