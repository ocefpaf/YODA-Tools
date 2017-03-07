from DataLoader.View.WizardSummaryPageView import WizardSummaryPageView


class WizardSummaryPageController(WizardSummaryPageView):
    def __init__(self, parent, title):
        super(WizardSummaryPageController, self).__init__(parent)
        self.title = title