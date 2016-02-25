'''
Created on Jan 13, 2015

@author: oly
'''
import unittest
from indicators.indicators import RSI
from indicators.stochastics import Stochastics
from stocklib.perioddata import PeriodData


class IndicatorsTest(unittest.TestCase):
    def _fakePeriodData(self, close):
        return PeriodData(stock="SPY", date=None, open=close, high=close, low=close, close=close, adjustedClose=close, volume=1000000, period=60*60*24)

    def _fakePeriodOHLCData(self, open, high, low, close):
        return PeriodData(stock="SPY", date=None, open=open, high=high, low=low, close=close, adjustedClose=close, volume=1000000, period=60*60*24)

    def testRSI(self):
        rsi = RSI(14)
        for close in []:
            rsi.handle(self._fakePeriodData(close))
        self.assertTrue(rsi.ready())
        self.assertTrue(rsi.value() < 67 and rsi.value() > 65)

    def testStochastics(self):
        """
        Testing the Stochastic indicator to see if it performs per standard.

        See: http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:stochastic_oscillator_fast_slow_and_full

        """
        stoch = Stochastics(14,1,3)
        # high,low - open does not matter and close only
        # relevant for last bar
        for bar in [
                (127.01, 125.36),
                (127.62, 126.16),
                (126.59, 124.93),
                (127.35, 126.09),
                (128.17, 126.82),
                (128.43, 126.48),
                (127.37, 126.03),
                (126.42, 124.83),
                (126.90, 126.39),
                (126.85, 125.72),
                (125.65, 124.56),
                (125.72, 124.57),
                (127.16, 125.07)]:
            stoch.handle(self._fakePeriodOHLCData(bar[0], bar[0], bar[1], bar[1]))
        stoch.handle(self._fakePeriodOHLCData(127.72, 127.72, 126.86, 127.29))
        stoch.handle(self._fakePeriodOHLCData(127.69, 127.69, 126.83, 127.18))
        stoch.handle(self._fakePeriodOHLCData(128.22, 128.22, 126.80, 128.01))
        self.assertTrue(stoch.ready())
        self.assertLess(abs(stoch.percentK()-89.20), .1)

if __name__ == "__main__":
    unittest.main()