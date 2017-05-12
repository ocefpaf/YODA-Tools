import os
import unittest

import openpyxl

from yodatools.converter.Inputs.excelInput import ExcelInput


class ExcelTest(unittest.TestCase):

    def setUp(self):
        self.before_each_do()

    def before_each_do(self):
        curr_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        file_path = os.path.join(curr_folder, 'test_files', 'YODA_TimeSeriesSpecimen_RB_2014-15_pub.xlsx')

        if not does_file_exit(file_path):
            print file_path + " does not exist"
            assert False

        self.excel = ExcelInput(file_path)

    def test_excel_parsing(self):
        self.assertTrue(self.excel.parse())


def does_file_exit(file_path):
    if os.path.isfile(file_path):
        return True
    return False
