from DataLoader.View.WizardHomePageView import WizardHomePageView


class WizardHomePageController(WizardHomePageView):
    def __init__(self, parent, title=""):
        super(WizardHomePageController, self).__init__(parent)
        self.parent = parent
        self.title = title
        self.pages_enabled = {0: True}

    def on_check_box(self, event):
        self.pages_enabled[event.GetId()] = event.Checked()
