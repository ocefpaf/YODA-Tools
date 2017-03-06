from DataLoader.View.WizardHomePageView import WizardHomePageView


class WizardHomePageController(WizardHomePageView):
    def __init__(self, parent, title=""):
        super(WizardHomePageController, self).__init__(parent)
        self.title = title