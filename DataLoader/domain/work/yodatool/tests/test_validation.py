__author__ = 'cyoun'
import logging
import os.path
import unittest

import yaml

# curr_folder = os.path.abspath(os.path.dirname(__file__))
# sys.path.insert(0, '%s/../' % curr_folder)
# print curr_folder

logger = logging.getLogger("Test.YODATool")

from DataLoader.domain.work.yodatool import TSvalidator
from DataLoader.domain.work.yodatool import CVvalidator

from ._utils import (
    check_excell_installed)

is_excel_installed = check_excell_installed()

class validateYodaTestCases(unittest.TestCase):

    def setUp(self):
        # yodafile='./yodatool/examples/YODA_TimeSeries_Example1_Template_0.3.1-alpha.yaml'

        curr_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        yodafile = os.path.join(curr_folder, 'examples','YODA_TimeSeries_Example1_Template_0.3.1-alpha.yaml' )

        stream = file(yodafile)
        yaml_data = yaml.load(stream)

        if 'YODA' in yaml_data:
            yaml_data.pop('YODA')

        self.data = yaml_data

    def test_dataTypes(self):

        tsvalidator = TSvalidator(logger)
        flag = tsvalidator.validate(3,self.data)

        self.assertTrue(flag, 'Data type validation is OK.')

    def test_controlledVocaburary(self):
        cvvalidator = CVvalidator(logger)
        flag = cvvalidator.validate(self.data)

        self.assertTrue(flag,'CV validation is OK.' )

if __name__ == '__main__':
    unittest.main()
