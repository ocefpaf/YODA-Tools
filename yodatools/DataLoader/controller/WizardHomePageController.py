import wx

from yodatools.DataLoader import WizardHomePageView


class WizardHomePageController(WizardHomePageView):
    def __init__(self, parent, title=""):
        super(WizardHomePageController, self).__init__(parent)
        self.parent = parent
        self.title = title
        self.pages_enabled = {0: True}

    def on_check_box(self, event):
        self.pages_enabled[event.GetId()] = event.Checked()
        if True in self.pages_enabled.values()[1:4]:
            self.GetTopLevelParent().next_button.Enable()
        else:
            self.GetTopLevelParent().next_button.Disable()

    def on_browse_button(self, event):
        wildcards = "All File (*.*) | *.*"

        dialog = wx.FileDialog(self,
                               message="Add file",
                               wildcard=wildcards,
                               style=wx.FD_CHANGE_DIR)

        if dialog.ShowModal() != wx.ID_OK:
            return

        self.input_file_text_ctrl.SetValue(dialog.GetPath())
