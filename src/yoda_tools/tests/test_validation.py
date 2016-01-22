__author__ = 'cyoun'
import unittest
import sys
import os.path

curr_folder = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, '%s/../../../' % curr_folder)
print curr_folder

from src.yoda_tools.yoda import validate_timeseries

class validateYodaTestCases(unittest.TestCase):
    def test_goodFile(self, file='../examples/YODA_TimeSeries_Example1_Template_0.3.1-alpha.yaml'):
        flag =  validate_timeseries(file)
        self.assertTrue(flag, 'YODA_TimeSeries_Example1_Template_0.3.1-alpha.yaml failed')

    def test_badFile(self, file='../examples/YODA_TimeSeries_Example1_Template_0.3.0-alpha.yaml'):
        flag =  validate_timeseries(file)
        self.assertFalse(flag,'YODA_TimeSeries_Example1_Template_0.3.0-alpha.yaml failed to find errors' )

