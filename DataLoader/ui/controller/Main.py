import wx
from DataLoader.ui.controller.WizardController import WizardController


if __name__ == '__main__':
    app = wx.App()
    controller = WizardController(None)
    controller.CenterOnScreen()
    controller.Show()
    app.MainLoop()
