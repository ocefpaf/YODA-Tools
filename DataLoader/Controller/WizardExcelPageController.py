from DataLoader.View.WizardExcelPageView import WizardExcelPageView


class WizardExcelPageController(WizardExcelPageView):
    def __init__(self, parent, title=""):
        super(WizardExcelPageController, self).__init__(parent)
        self.title = title
