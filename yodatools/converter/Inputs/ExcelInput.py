import os
import time

import openpyxl
from openpyxl.cell.cell import get_column_letter
from odm2api.ODM2.models import *

from yodatools.converter.Abstract import iInputs
import xlrd
import pandas


class ExcelInput(iInputs):
    # https://automatetheboringstuff.com/chapter12/
    def __init__(self, input_file, output_file=None):
        super(ExcelInput, self).__init__()
        self.input_file = input_file

        # self.workbook.get_named_range('Organizations_Table').attr_text

        if output_file is None:
            output_file = "export.csv"

        self.output_file = output_file
        self.workbook = None
        self.sheets = []
        self.name_ranges = None
        self.tables = {}

    def get_table_name_ranges(self):
        """
        Returns a list of the name range that have a table.
        The name range should contain the cells locations of the data.
        :rtype: list
        """
        CONST_NAME = "_Table"
        table_name_range = {}
        for name_range in self.name_ranges:
            if CONST_NAME in name_range.name:
                sheet = name_range.attr_text.split('!')[0]
                sheet = sheet.replace('\'', '')

                if sheet in table_name_range:
                    table_name_range[sheet].append(name_range)
                else:
                    table_name_range[sheet] = [name_range]

        return table_name_range

    def parse(self, file_path=None):
        if not self.verify(file_path):
            print "Something is wrong with the file but what?"
            return

        self.tables = self.get_table_name_ranges()
        methods = self.parse_methods()
        variables = self.parse_variables()
        specimens = self.parse_specimens()
        units = self.parse_units()
        processing_levels = self.parse_processing_level()
        # sampling_feature = self.parse_sampling_feature()
        data_values = self.read_data_values()

    def parse_units(self):

        CONST_UNITS = 'Units'

        if CONST_UNITS not in self.tables:
            return []

        sheet = self.workbook.get_sheet_by_name(CONST_UNITS)
        tables = self.tables[CONST_UNITS]

        units = []
        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]
            cells = cells[1:]  # Remove the column names

            for row in cells:
                unit = Units()
                unit.UnitsTypeCV = row[0].value
                unit.UnitsAbbreviation = row[1].value
                unit.UnitsName = row[2].value
                unit.UnitsLink = row[3].value
                units.append(unit)

        return units

    def read_data_values(self):
        dataframes = pandas.read_excel(io=self.input_file, sheetname='Data Values')
        print dataframes

    def parse_processing_level(self):
        CONST_PROC_LEVEL = 'Processing Levels'

        if CONST_PROC_LEVEL not in self.tables:
            return []

        sheet = self.workbook.get_sheet_by_name(CONST_PROC_LEVEL)
        tables = self.tables[CONST_PROC_LEVEL]

        processing_levels = []
        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]
            cells = cells[1:]  # Remove the column names

            for row in cells:
                proc_lvl = ProcessingLevels()
                proc_lvl.ProcessingLevelCode = row[0].value
                proc_lvl.Definition = row[1].value
                proc_lvl.Explanation = row[2].value
                processing_levels.append(proc_lvl)

        return processing_levels

    def parse_sampling_feature(self):
        CONST_SAMP_FEAT = 'Sampling Features'

        if CONST_SAMP_FEAT not in self.tables:
            return []

        sheet = self.workbook.get_sheet_by_name(CONST_SAMP_FEAT)
        tables = self.tables[CONST_SAMP_FEAT]

        sampling_features = []
        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]
            cells = cells[1:]  # Remove the column names

            for row in cells:
                sf = SamplingFeatures()
                sampling_features.append(sf)

        return sampling_features

    def parse_specimens(self):
        CONST_SPECIMENS = 'Specimens'

        if CONST_SPECIMENS not in self.tables:
            return []

        sheet = self.workbook.get_sheet_by_name(CONST_SPECIMENS)
        tables = self.tables[CONST_SPECIMENS]

        specimens = []
        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]
            cells = cells[1:]  # Remove the column names

            for row in cells:
                sp = Specimens()
                sp.SamplingFeatureUUID = row[0].value
                sp.SamplingFeatureCode = row[1].value
                sp.SamplingFeatureName = row[2].value
                sp.SamplingFeatureDescription = row[3].value
                sp.SamplingFeatureTypeCV = row[4].value
                sp.SpecimenMediumCV = row[5].value
                sp.IsFieldSpecimen = row[6].value
                specimens.append(sp)

        return specimens

    def parse_methods(self):
        # tables = self.get_tables_in_sheet('Methods')

        CONST_METHODS = "Methods"

        if CONST_METHODS not in self.tables:
            return []

        sheet = self.workbook.get_sheet_by_name(CONST_METHODS)
        tables = self.tables[CONST_METHODS]

        methods = []
        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]
            cells = cells[1:]  # Remove the column names

            for row in cells:
                method = Methods()
                method.MethodTypeCV = row[0].value
                method.MethodCode = row[1].value
                method.MethodName = row[2].value
                method.MethodDescription = row[3].value
                method.MethodLink = row[4].value

                org = Organizations()
                org.OrganizationName = row[5].value
                method.OrganizationObj = org

                methods.append(method)

        return methods

    def get_tables_in_sheet(self, sheet_name):
        """
        :param sheet_name: 
        :rtype: list
        :return:
        """

        if sheet_name not in self.sheets:
            print "%s not in excel sheet" % sheet_name
            return IndexError

        sheet = self.workbook.get_sheet_by_name(sheet_name)
        tables = []
        # sheet['A1:B3']
        for table in sheet._tables:
            top_left_cell, bottom_right_cell = table.ref.split(':')
            tables.append(sheet[top_left_cell: bottom_right_cell])
        return tables

    def parse_variables(self):

        CONST_VARIABLES = "Variables"

        if CONST_VARIABLES not in self.tables:
            return []

        sheet = self.workbook.get_sheet_by_name(CONST_VARIABLES)
        tables = self.tables[CONST_VARIABLES]

        variables = []
        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]
            cells = cells[1:]  # Remove the column names
            for row in cells:
                var = Variables()
                var.VariableTypeCV = row[0].value
                var.VariableCode = row[1].value
                var.VariableNameCV = row[2].value
                var.VariableDefinition = row[3].value
                var.SpeciationCV = row[4].value
                var.NoDataValue = row[5].value
                variables.append(var)

        return variables

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

        self.workbook = openpyxl.load_workbook(self.input_file, read_only=True)
        self.name_ranges = self.workbook.get_named_ranges()
        self.sheets = self.workbook.get_sheet_names()

        # self.name_ranges[0].destinations.next()
        # self.name_ranges[1].attr_text
        # 'INDEX(ControlledVocabularies[actiontype],1,1):INDEX(ControlledVocabularies[actiontype],COUNTA(ControlledVocabularies[actiontype]))'

        return True

    def sendODM2Session(self):
        pass
