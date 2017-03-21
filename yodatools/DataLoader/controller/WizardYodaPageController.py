from yodatools.DataLoader import WizardYodaPage


class WizardYodaPageController(WizardYodaPage):
    def __init__(self, parent, title=""):
        super(WizardYodaPageController, self).__init__(parent)
        self.title = title
