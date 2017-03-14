from DataLoader.View.WizardView import WizardView
from WizardHomePageController import WizardHomePageController
from WizardYodaPageController import WizardYodaPageController
from WizardExcelPageController import WizardExcelPageController
from WizardDatabasePageController import WizardDatabasePageController
from WizardSummaryPageController import WizardSummaryPageController
import wx


class WizardController(WizardView):
    def __init__(self, parent):
        super(WizardController, self).__init__(parent)
        self.parent = parent
        self.yoda_page = WizardYodaPageController(self.body_panel, title="Yoda")
        self.excel_page = WizardExcelPageController(self.body_panel, title="Excel")
        self.database_page = WizardDatabasePageController(self.body_panel, title="ODM2")
        self.summary_page = WizardSummaryPageController(self, self.body_panel, title="Summary")
        self.home_page = WizardHomePageController(self.body_panel, title="Loader Wizard")

        # The key must match the checkbox id
        self.home_page.pages_enabled = {
            0: True,   # home page
            1: False,  # yoda page
            2: False,  # excel page
            3: False,  # database page
            4: True    # summary page
        }

        self.add_page(self.home_page)
        self.add_page(self.yoda_page)
        self.add_page(self.excel_page)
        self.add_page(self.database_page)
        self.add_page(self.summary_page)
        self.next_button.Disable()

        self.show_home_page()
        self.SetSize((450, 450))

    def on_next_button(self, event):
        if self.page_number + 2 > len(self.wizard_pages):
            self.summary_page.run()
            self.Close()

        self.wizard_pages[self.page_number].Hide()

        # Boundary checking
        self.page_number = min(self.page_number + 1, len(self.wizard_pages) - 1)

        if not self.home_page.pages_enabled[self.page_number]:
            self.page_number = self.__go_to_next_available_page(forward=True)

        self.__update_page()

    def __go_to_next_available_page(self, forward=True):
        if forward:
            for i in range(self.page_number, len(self.home_page.pages_enabled.values())):
                if self.home_page.pages_enabled[i]:
                    return i
        else:
            for i in range(self.page_number, -1, -1):
                if self.home_page.pages_enabled[i]:
                    return i

        return 0

    def on_back_button(self, event):
        self.wizard_pages[self.page_number].Hide()

        # Boundary checking
        self.page_number = max(self.page_number - 1, 0)

        if not self.home_page.pages_enabled[self.page_number]:
            self.page_number = self.__go_to_next_available_page(forward=False)

        self.__update_page()

    def __update_page(self):
        self.title_text.SetLabel(self.wizard_pages[self.page_number].title)

        if self.page_number == 0:
            self.will_flip_to_first_page()
        elif self.page_number == len(self.wizard_pages) - 1:
            self.will_flip_to_last_page()
        else:
            self.next_button.SetLabel("Next")
            self.back_button.Show()

        self.wizard_pages[self.page_number].Show()
        self.body_panel.Layout()
        self.footer_panel.Layout()

    def will_flip_to_first_page(self):
        self.back_button.Hide()

    def will_flip_to_last_page(self):
        self.next_button.SetLabel("Finish")
        self.back_button.Show()

    def show_home_page(self):
        for page in self.wizard_pages:
            page.Hide()

        self.page_number = 0
        self.__update_page()
