from yodatools.converter.Inputs.excelInput import ExcelInput
from yodatools.converter.Inputs.yamlInput import yamlInput
from yodatools.converter.Outputs.yamlOutput import yamlOutput
from yodatools.converter.Outputs.dbOutput import dbOutput
from yodatools.dataloader.view.WizardSummaryPageView import WizardSummaryPageView


class WizardSummaryPageController(WizardSummaryPageView):

    def __init__(self, parent, panel, title):
        super(WizardSummaryPageController, self).__init__(panel)
        self.parent = parent
        self.title = title

    def run(self, input_file, yoda_output_file_path=None, odm2_connection=None, sqlite_connection = None):

        # Start gauge with 2% to show starting progress
        self.gauge.SetValue(2)

        # Check if it is a yaml, or excel file
        file_type = verify_file_type(input_file)

        if file_type == 'invalid':  # Accept only excel and yaml files
            print('File extension invalid or no file')
            return

        if file_type == 'excel':
            kwargs = {'gauge': self.gauge}
            excel = ExcelInput()
            excel.parse(input_file, **kwargs)
            session = excel.sendODM2Session()
        else:
            # Must be a yoda file
            yoda = yamlInput(input_file)
            yoda.parse(input_file)
            session = yoda.sendODM2Session()

        self.gauge.SetValue(50)
        print "Input complete"
        # Go through each checkbox
        if yoda_output_file_path is not None:
            yaml = yamlOutput()
            yaml.save(session=session, file_path=yoda_output_file_path)
            print "Yoda Output Complete"

        if odm2_connection is not None:
            db = dbOutput()
            db.save(session=session, connection_string=odm2_connection)
            print "DB Output Complete"

        if sqlite_connection is not None:
            db = dbOutput()
            db.save(session=session, connection_string=sqlite_connection)
            print "SQLite Output Complete"

        session.close_all()

        self.gauge.SetValue(100)
        self.parent.load_finished_execution()
        return


def verify_file_type(input_file):
    CONST_LEGAL_EXCEL_EXTENSIONS = ('xlsx', 'xlsm')

    if input_file.endswith(CONST_LEGAL_EXCEL_EXTENSIONS):
        file_type = 'excel'
    elif input_file.endswith('yml'):
        file_type = 'yaml'
    else:
        file_type = 'invalid'

    return file_type
