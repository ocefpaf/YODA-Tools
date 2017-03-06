from DataLoader.View.WizardView import WizardView
from WizardHomePageController import WizardHomePageController
from WizardYodaPageController import WizardYodaPageController
from WizardExcelPageController import WizardExcelPageController
from WizardDatabasePageController import WizardDatabasePageController


class WizardController(WizardView):
    def __init__(self, parent):
        super(WizardController, self).__init__(parent)

        self.home_page = WizardHomePageController(self.body_panel)
        self.yoda_page = WizardYodaPageController(self.body_panel)
        self.excel_page = WizardExcelPageController(self.body_panel)
        self.database_page = WizardDatabasePageController(self.body_panel)

        self.add_page(self.home_page)
        self.add_page(self.yoda_page)
        self.add_page(self.excel_page)
        self.add_page(self.database_page)

        self.show_home_page()

    def on_next_button(self, event):
        self.wizard_pages[self.page_number].Hide()

        # Boundary checking
        self.page_number = min(self.page_number + 1, len(self.wizard_pages) - 1)

        self.wizard_pages[self.page_number].Show()
        self.body_panel.Layout()

    def on_back_button(self, event):
        self.wizard_pages[self.page_number].Hide()

        # Boundary checking
        self.page_number = max(self.page_number - 1, 0)
        self.wizard_pages[self.page_number].Show()
        self.body_panel.Layout()

    def show_home_page(self):
        for page in self.wizard_pages:
            page.Hide()

        self.page_number = 0
        self.wizard_pages[self.page_number].Show()


