import wx
from DataLoader.Controller.WizardController import WizardController


if __name__ == '__main__':
    app = wx.App()
    controller = WizardController(None)
    controller.Show()
    app.MainLoop()