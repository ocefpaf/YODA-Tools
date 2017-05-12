import os
import openpyxl

from yodatools.converter.Abstract import iInputs
import time
from yodatools.excelparser.excelSpecimen import ExcelSpecimen
from yodatools.excelparser.excelTimeseries import ExcelTimeseries


class ExcelInput(iInputs):
    def __init__(self, input_file, **kwargs):
        super(ExcelInput, self).__init__(input_file)

        self.input_file = input_file
        self.output_file = "export.csv"
        self.gauge = None


        if 'output_file' in kwargs:
            self.output_file = kwargs['output_file']

        if 'gauge' in kwargs:
            self.gauge = kwargs['gauge']



#     def parse(self, file_path=None):
    def parse(self, file_path=None):
        """
        If any of the methods return early, then check that they have the table ranges
        The table range should exist in the tables from get_table_name_range()
        :param file_path:
        :return:
        """

        if not self.verify(file_path):
            print "Something is wrong with the file but what?"
            return False

        type = self.get_type(file_path)

        start = time.time()

        if type == "TimeSeries":
            raise Exception("TimeSeries Parsing is not currently supported")
            et = ExcelTimeseries(self.input_file, gauge=self.gauge)
            et.parse(self._session)
        else:
            es = ExcelSpecimen(self.input_file, gauge=self.gauge)
            es.parse(self._session)


        # self._session.commit()

        end = time.time()
        # print(end - start)

        return True

    def get_type(self, file_path):

        self.workbook = openpyxl.load_workbook(self.input_file, read_only=True)
        self.name_ranges = self.workbook.get_named_ranges()
        self.sheets = self.workbook.get_sheet_names()
        # cells = self.sheets[0][org_table.attr_text.split('!')[1].replace('$', '')]
        if "Instructions" in self.sheets:
            named_range = "TemplateProfile"
            sheet = "Instructions"
            return "TimeSeries"
        else:
            return "SpecimenTimeSeries"


    def verify(self, file_path=None):

        if file_path is not None:
            self.input_file = file_path

        if not os.path.isfile(self.input_file):
            print "File does not exist"
            return False

        self.workbook = openpyxl.load_workbook(self.input_file, read_only=True)
        self.name_ranges = self.workbook.get_named_ranges()
        self.sheets = self.workbook.get_sheet_names()

        return True

    def sendODM2Session(self):  # this should be renamed to get not send because it returns a value
        return self._session
