import os
import unittest

import openpyxl

from yodatools.converter.Inputs.ExcelInput import ExcelInput


class ExcelTest(unittest.TestCase):

    def setUp(self):
        self.before_each_do()

    def before_each_do(self):
        curr_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        file_path = os.path.join(curr_folder, 'test_files', 'YODA_TimeSeriesSpecimen_RB_2014-15_pub.xlsx')

        if not does_file_exit(file_path):
            assert False
        self.excel = ExcelInput(file_path)

        self.session = self.excel.sendODM2Session()
        self.workbook = openpyxl.load_workbook(file_path, data_only=True)
        self.name_ranges = self.workbook.get_named_ranges()
        self.sheets = self.workbook.get_sheet_names()

    def test_stuff(self):
        print 123
        sheet = self.workbook.get_sheet_by_name('Controlled Vocabularies')
        print sheet.get_cell_collection()[0]


def does_file_exit(file_path):
    if os.path.isfile(file_path):
        return True
    return False
