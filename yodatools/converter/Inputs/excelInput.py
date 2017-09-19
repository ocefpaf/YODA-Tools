import os

import openpyxl

from yodatools.converter.Abstract import iInputs
from yodatools.excelparser.excelSpecimen import ExcelSpecimen
from yodatools.excelparser.excelTimeseries import ExcelTimeseries


class ExcelInput(iInputs):
    def __init__(self, **kwargs):
        super(ExcelInput, self).__init__()

        self.output_file = 'export.csv'
        self.gauge = None

        if 'output_file' in kwargs:
            self.output_file = kwargs['output_file']

        if 'gauge' in kwargs:
            self.gauge = kwargs['gauge']

    def parse(self, file_path):
        """
        If any of the methods return early,
        then check that they have the table ranges
        The table range should exist in the tables from get_table_name_range()

        :param file_path:
        :return:

        """
        self.file_path = file_path
        if not self.verify(self.file_path):
            print('Something is wrong with the file but what?')
            return False

        yoda_type = self.get_type(self.file_path)

        if yoda_type == 'TimeSeries':
            raise Exception('TimeSeries Parsing is not currently supported')
            et = ExcelTimeseries(self.file_path, gauge=self.gauge)
            et.parse(self._session)
        else:
            es = ExcelSpecimen(self.file_path, gauge=self.gauge)
            es.parse(self._session)
        # self._session.commit()
        return True

    def get_type(self, file_path):
        self.workbook = openpyxl.load_workbook(file_path, read_only=True)
        self.name_ranges = self.workbook.get_named_ranges()
        self.sheets = self.workbook.get_sheet_names()
        # cells = self.sheets[0][org_table.attr_text.split('!')[1].replace('$', '')]  # noqa
        if 'Instructions' in self.sheets:
            # FIXME: The next two lines assign variables that are note used.
            # named_range = 'TemplateProfile'
            # sheet = 'Instructions'
            return 'TimeSeries'
        else:
            return 'SpecimenTimeSeries'

    def verify(self, file_path=None):

        if file_path is not None:
            self.input_file = file_path

        if not os.path.isfile(self.input_file):
            print('File does not exist')
            return False

        self.workbook = openpyxl.load_workbook(file_path, read_only=True)
        self.name_ranges = self.workbook.get_named_ranges()
        self.sheets = self.workbook.get_sheet_names()

        return True

    # This should be renamed to get not send because it returns a value.
    def sendODM2Session(self):
        return self._session
