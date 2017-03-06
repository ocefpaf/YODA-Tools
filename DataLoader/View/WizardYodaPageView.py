import wx


class WizardYodaPage(wx.Panel):
    def __init__(self, parent):
        super(WizardYodaPage, self).__init__(parent)

        self.SetBackgroundColour(wx.BLUE)
        self.Hide()