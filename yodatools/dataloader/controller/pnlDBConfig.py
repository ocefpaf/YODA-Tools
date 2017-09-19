"""Subclass of clsDBConfiguration, which is generated by wxFormBuilder."""

import wx

from yodatools.dataloader.view.clsDBConfig import clsDBConfiguration


class frmDBConfig(wx.Dialog):
    def __init__(self, parent, service_manager, is_main=False):
        wx.Dialog.__init__(
            self,
            parent,
            title='Database Configuration',
            style=wx.DEFAULT_DIALOG_STYLE, size=wx.Size(500, 315)
        )
        self.panel = pnlDBConfig(self, service_manager, is_main)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.AddWindow(self.panel, 1, border=1, flag=wx.EXPAND | wx.GROW | wx.ALL)  # noqa
        self.SetSizer(self.sizer)
        self.sizer.Fit(self.panel)


# Implementing clsDBConfiguration
class pnlDBConfig(clsDBConfiguration):
    def __init__(self, parent, service_manager, is_main=False):
        clsDBConfiguration.__init__(self, parent)

        self.choices = {
            'Microsoft SQL Server': 'mssql',
            'MySQL': 'mysql',
            'PostgreSQL': 'postgresql',
            'SQLite': 'sqlite'
        }
        self.cbDatabaseType.AppendItems(self.choices.keys())

        self.parent = parent
        self.is_main = is_main
        self.service_manager = service_manager

        self.set_field_values()

    def OnValueChanged(self, event):
        """

        :param event:
        :return:

        """
        self.btnSave.Enable(False)

        try:
            curr_dict = self.getFieldValues()
            if self.conn_dict == curr_dict:
                self.btnSave.Enable(True)
        except:
            pass

    # Handlers for clsDBConfiguration events.
    def OnBtnTest(self, event):
        conn_dict = self.getFieldValues()
        if self.validateInput(conn_dict):
            self.btnSave.Enable(True)
            self.conn_dict = conn_dict

    def OnBtnSave(self, event):

        # self.parent.EndModal(wx.ID_OK)
        raise NotImplementedError

    def OnBtnCancel(self, event):
        self.parent.SetReturnCode(wx.ID_CANCEL)
        self.parent.EndModal(wx.ID_CANCEL)

    def validateInput(self, conn_dict):
        message = ''

        # Check that everything has been filled out.
        if not all(x for x in conn_dict.values()):
            message = 'Please complete every field in order to proceed'
            wx.MessageBox(message, 'Database Connection', wx.OK | wx.ICON_EXCLAMATION)  # noqa
            return False

        try:
            if self.service_manager.test_connection(conn_dict):
                message = 'This connection is valid'
                wx.MessageBox(message, 'Test Connection', wx.OK)
            else:
                # TODO: add error message if user cannot connect to the
                # database (not using VPN) but the db is still 1.1.1.
                if not (self.service_manager.get_db_version(conn_dict)):
                    message = 'Cannot connect to the database'
                else:
                    message = 'This connection is not a 1.1.1 Database'

                wx.MessageBox(message, 'Error Occurred', wx.OK | wx.ICON_ERROR)
                return False
        except Exception as e:
            print (e)
            wx.MessageBox('This connection is invalid', 'Error Occurred', wx.ICON_ERROR | wx.OK)  # noqa
            return False
            # wx.MessageBox(e.message, 'Error Occurred', wx.ICON_ERROR | wx.OK)

        return True

    # Returns a dictionary of the database values entered in the form
    def getFieldValues(self):
        conn_dict = {}

        conn_dict['engine'] = self.choices[self.cbDatabaseType.GetValue()]
        conn_dict['user'] = self.txtUser.GetValue()
        conn_dict['password'] = self.txtPass.GetValue()
        conn_dict['address'] = self.txtServer.GetValue()
        conn_dict['db'] = self.txtDBName.GetValue()
        conn_dict['version'] = ''

        return conn_dict

    def set_field_values(self):
        if self.service_manager is not None:
            conn = self.service_manager.is_valid_connection()
            if conn is not None:
                self.txtServer.SetValue(conn['address'])
                self.txtDBName.SetValue(conn['db'])
                self.txtUser.SetValue(conn['user'])

                for k, v in self.choices.iteritems():
                    if v == conn['engine']:
                        self.cbDatabaseType.SetValue(k)
