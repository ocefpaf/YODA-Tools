import wx


class WizardHomePageView(wx.Panel):
    def __init__(self, parent):
        super(WizardHomePageView, self).__init__(parent)
        self.SetBackgroundColour(wx.YELLOW)

        # Create components
        instructions_text = wx.StaticText(self, label="Load YODA file or Excel Template")
        self.input_file_text_ctrl = wx.TextCtrl(self)
        self.browse_button = wx.Button(self, label="Browse")

        # Sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Add components to sizer
        input_sizer.Add(self.input_file_text_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        input_sizer.Add(self.browse_button, 0, wx.EXPAND | wx.ALL, 0)

        sizer.Add(instructions_text, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(input_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

        self.Hide()