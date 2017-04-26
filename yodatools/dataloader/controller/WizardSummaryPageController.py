from yodatools.dataloader.view.WizardSummaryPageView import WizardSummaryPageView
from yodatools.converter.Inputs.ExcelInput import ExcelInput
from yodatools.converter.Inputs.yamlInput import yamlInput


class WizardSummaryPageController(WizardSummaryPageView):
    def __init__(self, parent, panel, title):
        super(WizardSummaryPageController, self).__init__(panel)
        self.parent = parent
        self.title = title

    def run(self, selection):
        if 'excel' in selection:
            # excel_page = selection['excel']
            input_file = self.parent.home_page.input_file_text_ctrl.GetValue()

            # check what kind of input file it is. is it a yaml or excel. Check extension
            # if excel do below
            excel = ExcelInput(input_file)
            excel.parse()
            session = excel.sendODM2Session()

            """
            go through each checkboxes 
            grey out excel template. they can choose yoda or odm2db
            
            if yoda is checked
                get yoda file path
                call yoda export. which is in yodatools->converter->outputs sending in session
                
                 save(self, session, file_path):
             if database is checked
                create connection string
                call dboutput and do same as yoda export and send in connection string as filepath
            
            """
