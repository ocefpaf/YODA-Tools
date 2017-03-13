import os
import openpyxl
from DataLoader.Model.Abstract import iInputs


class ExcelInput(iInputs):
    def __init__(self, input_file, output_file=None):
        super(ExcelInput, self).__init__()
        self.input_file = input_file

        if output_file is None:
            output_file = "export.csv"

        self.output_file = output_file
        self.sheets = None

    def parse(self, file_path=None):

        if file_path is None:
            self.input_file = file_path

        if not os.path.isfile(self.input_file):
            print "File does not exist"
            return

        workbook = openpyxl.load_workbook(self.input_file, read_only=True)
        self.sheets = workbook.get_sheet_names()
        print workbook.get_sheet_by_name[self.sheets[0]]

    def verify(self):
        pass

    def sendODM2Session(self):
        pass