import wx
from yodatools.dataloader.controller.WizardController import WizardController

import pyodbc
import psycopg2

def main():
    app = wx.App()
    controller = WizardController(None)
    controller.CenterOnScreen()
    controller.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
