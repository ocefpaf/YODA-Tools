import wx


class WizardDatabasePageView(wx.Panel):
    def __init__(self, parent):
        super(WizardDatabasePageView, self).__init__(parent)

        # Components
        instructions_text = wx.StaticText(self, label="Connect to a database")
        self.database_combo = wx.ComboBox(self, style=wx.CB_READONLY)
        self.address_text_ctrl = wx.TextCtrl(self)
        self.username_text_ctrl = wx.TextCtrl(self)
        self.password_text_ctrl = wx.TextCtrl(self, style=wx.TE_PASSWORD)

        # Style componets
        self.address_text_ctrl.SetHint("Address")
        self.username_text_ctrl.SetHint("Username")
        self.password_text_ctrl.SetHint("Password")

        # Sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Add Components to sizer
        sizer.Add(instructions_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)
        sizer.Add(self.database_combo, 0, wx.EXPAND | wx.ALL ^ wx.BOTTOM ^ wx.TOP, 15)
        sizer.Add(self.address_text_ctrl, 0, wx.EXPAND | wx.ALL ^ wx.BOTTOM, 15)
        sizer.Add(self.username_text_ctrl, 0, wx.EXPAND | wx.ALL ^ wx.BOTTOM, 15)
        sizer.Add(self.password_text_ctrl, 0, wx.EXPAND | wx.ALL ^ wx.BOTTOM, 15)

        horizontal_sizer.Add(sizer, 1, wx.ALIGN_CENTER_VERTICAL)

        self.SetSizer(horizontal_sizer)
        self.Hide()
