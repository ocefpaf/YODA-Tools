__author__ = 'cyoun'
import unittest
import argparse
import src.yoda_tools.yoda as yoda

class validateYodaTestCases(unittest.TestCase):
    def test_goodFile(self, file='../../examples/Timeseries_Template_Working_my_version.yaml'):
        flag =  yoda.validate_timeseries(file)
        self.assertTrue(flag, 'Timeseries_Template_Working_my_version.yaml failed')

    def test_badFile(self, file='../../examples/Timeseries_Template_Working.yaml'):
        flag =  yoda.validate_timeseries(file)
        self.assertFalse(flag,'Timeseries_Template_Working.yaml failed to find errors' )

