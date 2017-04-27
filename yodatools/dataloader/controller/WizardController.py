from WizardDatabasePageController import WizardDatabasePageController
from WizardExcelPageController import WizardExcelPageController
from WizardHomePageController import WizardHomePageController
from WizardSummaryPageController import WizardSummaryPageController
from WizardYodaPageController import WizardYodaPageViewController
from yodatools.dataloader.view.WizardView import WizardView
import threading


class WizardController(WizardView):
    def __init__(self, parent):
        super(WizardController, self).__init__(parent)
        self.parent = parent
        self.yoda_page = WizardYodaPageViewController(self.body_panel, title="Yoda")
        self.excel_page = WizardExcelPageController(self.body_panel, title="Excel")
        self.database_page = WizardDatabasePageController(self.body_panel, title="ODM2")
        self.summary_page = WizardSummaryPageController(self, self.body_panel, title="Summary")
        self.home_page = WizardHomePageController(self.body_panel, title="Loader Wizard")

        self.is_on_page_before_summary = False
        self.thread = threading.Thread()

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
           # self.summary_page.run(self.selected_pages())
            self.Close()

        self.wizard_pages[self.page_number].Hide()

        # Boundary checking
        self.page_number = self.__go_to_next_available_page(forward=True)
        self.__check_if_on_page_before_summary()

        self.__update_page()

    def __check_if_on_page_before_summary(self):
        self.is_on_page_before_summary = True
        for i in range(self.page_number + 1, len(self.home_page.pages_enabled.values()) - 1):
            if self.home_page.pages_enabled[i]:
                self.is_on_page_before_summary = False

    def __go_to_next_available_page(self, forward=True):
        if forward:
            for i in range(self.page_number, len(self.home_page.pages_enabled.values())):
                if self.home_page.pages_enabled[i] and i != self.page_number:
                    return i
        else:
            for i in range(self.page_number, -1, -1):
                if self.home_page.pages_enabled[i] and i != self.page_number:
                    return i

        return 0

    def on_back_button(self, event):
        self.wizard_pages[self.page_number].Hide()

        # Boundary checking
        self.page_number = self.__go_to_next_available_page(forward=False)
        self.__check_if_on_page_before_summary()

        self.__update_page()

    def __update_page(self):
        self.title_text.SetLabel(self.wizard_pages[self.page_number].title)

        if self.page_number == 0:
            self.will_flip_to_first_page()
        elif self.page_number == len(self.wizard_pages) - 1:
            self.will_flip_to_last_page()
            self.execute()  # Parse and save
        elif self.is_on_page_before_summary:
            self.will_flip_to_page_before_summary()
        else:
            self.next_button.SetLabel("Next")
            self.back_button.Show()

        self.wizard_pages[self.page_number].Show()
        self.body_panel.Layout()
        self.footer_panel.Layout()

    def will_flip_to_first_page(self):
        self.next_button.SetLabel("Next")
        self.back_button.Hide()

    def will_flip_to_last_page(self):
        self.next_button.SetLabel("Close")
        self.back_button.Show()

    def will_flip_to_page_before_summary(self):
        self.next_button.SetLabel("Finish")
        self.back_button.SetLabel("Cancel")
        self.back_button.Show()

    def show_home_page(self):
        for page in self.wizard_pages:
            page.Hide()

        self.page_number = 0
        self.__update_page()

    def selected_pages(self):
        pages = {}
        if self.home_page.pages_enabled[1]:
            pages['yoda'] = self.yoda_page
        if self.home_page.pages_enabled[2]:
            pages['excel'] = self.excel_page
        if self.home_page.pages_enabled[3]:
            pages['odm2'] = self.database_page

        return pages

    def execute(self):

        if not self.thread.isAlive():  # Prevent the thread from  being created twice!
            self.thread = threading.Thread(
                target=self.summary_page.run,
                args=(self.selected_pages()),
                name='execution_thread'
            )

            # When true, the thread will terminate when app is closed
            # When false, the thread will continue even after the ap is closed
            self.thread.setDaemon(True)
            self.thread.start()
            # self.summary_page.run(self.selected_pages())
        else:
            print "did not start another thread"
        # thread.join(timeout=2)
