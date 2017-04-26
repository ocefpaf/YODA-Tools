from yodatools.dataloader.view.WizardSummaryPageView import WizardSummaryPageView
from yodatools.converter.Inputs.ExcelInput import ExcelInput
from yodatools.converter.Inputs.yamlInput import yamlInput
from yodatools.converter.Outputs.yamlOutput import yamlOutput
from yodatools.converter.Outputs.dbOutput import dbOutput


class WizardSummaryPageController(WizardSummaryPageView):
    def __init__(self, parent, panel, title):
        super(WizardSummaryPageController, self).__init__(panel)
        self.parent = parent
        self.title = title

    def run(self, selections):

        input_file = self.parent.home_page.input_file_text_ctrl.GetValue()

        # Check if it is a yaml, or excel file
        file_type = verify_file_type(input_file)

        if file_type == 'invalid':  # Accept only excel and yaml files
            print "File extension is not valid"
            return

        session = None
        if file_type == 'excel':
            excel = ExcelInput(input_file)
            excel.parse()
            session = excel.sendODM2Session()
        else:
            # Must be a yoda file
            yoda = yamlInput()
            yoda.parse(input_file)

        # Go through each checkbox
        if 'excel' in selections:
            print 'export to an excel file has not been implemented'

        if 'yoda' in selections:
            print 'export to yoda'
            return
            # Before uncommenting the lines below, make sure the yamlOutput does not
            # overwrite the folder but instead creates a file

            # Get the directory to save the yaml output
            # yoda_export_path = selections['yoda'].file_text_ctrl.GetValue()
            # yaml = yamlOutput()
            # yaml.save(session=session, file_path=yoda_export_path)

        if 'odm2' in selections:
            print 'export to odm2'
            """
            create connection string
            call dboutput and do same as yoda export and send in connection string as filepath
            """


def verify_file_type(input_file):
    CONST_LEGAL_EXCEL_EXTENSIONS = ('xlsx', 'xlsm')

    if input_file.endswith(CONST_LEGAL_EXCEL_EXTENSIONS):
        file_type = 'excel'
    elif input_file.endswith('yml'):
        file_type = 'yaml'
    else:
        file_type = 'invalid'

    return file_type
