from yodatools.dataloader.view.WizardYodaPageView import WizardYodaPageView


class WizardYodaPageViewController(WizardYodaPageView):
    def __init__(self, parent, title=""):
        super(WizardYodaPageViewController, self).__init__(parent)
        self.title = title
