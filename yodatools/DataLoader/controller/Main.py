import wx

from yodatools.DataLoader import WizardController

if __name__ == '__main__':
    app = wx.App()
    controller = WizardController(None)
    controller.CenterOnScreen()
    controller.Show()
    app.MainLoop()