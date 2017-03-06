import wx


class WizardDatabasePageView(wx.Panel):
    def __init__(self, parent):
        super(WizardDatabasePageView, self).__init__(parent)
        self.SetBackgroundColour(wx.BLACK)
        self.Hide()
