import os
import time

import openpyxl
from openpyxl.cell.cell import get_column_letter

from yodatools.converter.Abstract import iInputs


class ExcelInput(iInputs):
    # https://automatetheboringstuff.com/chapter12/
    def __init__(self, input_file, output_file=None):
        super(ExcelInput, self).__init__()
        self.input_file = input_file

        if output_file is None:
            output_file = "export.csv"

        self.output_file = output_file
        self.workbook = None
        self.sheets = []
        self.name_ranges = None

    def parse(self, file_path=None):
        if not self.verify(file_path):
            print "Something is wrong with the file but what?"
            return

        # tables = self.get_tables_by_sheet('Methods')
        # methods = self.__extract_method()
        cells = self.get_cells_in_sheet("Specimens")

    def get_cells_in_sheet(self, sheet_name):
        sheet = self.workbook.get_sheet_by_name(sheet_name)
        table = self.get_tables_by_sheet(sheet_name)
        top_left_cell, bottom_right_cell = table[0].ref.split(':')
        return sheet[top_left_cell: bottom_right_cell]

    def __extract_method(self):

        if 'Methods' not in self.sheets:
            return

        method_sheet = self.workbook.get_sheet_by_name('Methods')

        # Find 'Method Information'
        row = 1
        found = False
        while not found and row < method_sheet.max_row:
            cell = method_sheet.cell(row=row, column=1)
            if cell.value is not None and 'Method Information' in cell.value:
                found = True
            row += 1

        # Find the last column that has the data
        col = 1
        while col < method_sheet.max_column:
            cell = method_sheet.cell(row=row, column=col)
            if not cell.value:
                col -= 1
                break
            col += 1

        top_left_coordinate = 'A' + str(row + 1)
        bottom_right_coordinate = get_column_letter(col) + str(method_sheet.max_row)
        method_information = method_sheet[top_left_coordinate: bottom_right_coordinate]

        return method_information

    def __extract_data_values(self):
        """
        Returns the data with its values but
        this could easily be changed to return the
        openpyxl cell object instead
        :return: dictionary
        """
        start = time.time()
        if 'Data Values' not in self.sheets:
            return

        data_sheet = self.workbook.get_sheet_by_name('Data Values')
        data = {
            'header': [],
            'values': [],
        }

        for i in range(1, data_sheet.max_column + 1):
            data['header'].append(data_sheet.cell(row=1, column=i).value)

        # data in openpyxl.cell objects
        # a = data_sheet['A2': get_column_letter(data_sheet.max_column) + str(data_sheet.max_row)]

        for i in range(2, data_sheet.max_row + 1):
            for j in range(1, data_sheet.max_column + 1):
                data['values'].append(data_sheet.cell(row=i, column=j).value)

            if i % 100 == 0:
                print i

        # data_sheet['A2': get_column_letter(data_sheet.max_column) + str(data_sheet.max_row)]

        end = time.time()
        print end - start

        return data

    def verify(self, file_path=None):

        if file_path is not None:
            self.input_file = file_path

        if not os.path.isfile(self.input_file):
            print "File does not exist"
            return False

        self.workbook = openpyxl.load_workbook(self.input_file, data_only=True)
        self.name_ranges = self.workbook.get_named_ranges()
        self.sheets = self.workbook.get_sheet_names()

        # self.name_ranges[0].destinations.next()
        # self.name_ranges[1].attr_text
        # 'INDEX(ControlledVocabularies[actiontype],1,1):INDEX(ControlledVocabularies[actiontype],COUNTA(ControlledVocabularies[actiontype]))'

        return True

    def get_tables_by_sheet(self, sheet_name):
        if sheet_name not in self.sheets:
            print "%s not in excel sheet" % sheet_name
            return IndexError

        return self.workbook.get_sheet_by_name(sheet_name)._tables

    def sendODM2Session(self):
        pass
