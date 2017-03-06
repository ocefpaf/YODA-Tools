import wx


class WizardExcelPageView(wx.Panel):
    def __init__(self, parent):
        super(WizardExcelPageView, self).__init__(parent)

        self.SetBackgroundColour(wx.GREEN)
        self.Hide()
