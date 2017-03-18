from DataLoader.ui.view.WizardExcelPageView import WizardExcelPageView


class WizardExcelPageController(WizardExcelPageView):
    def __init__(self, parent, title=""):
        super(WizardExcelPageController, self).__init__(parent)
        self.title = title
