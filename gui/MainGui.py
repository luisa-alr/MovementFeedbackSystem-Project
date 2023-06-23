import wx
from logic.StreamOverviewPanel import StreamOverviewPanel


class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)

        self.streamPanel = StreamOverviewPanel(self)
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)

        self.makeMenuBar()
        self.CreateStatusBar()
        self.SetStatusText("Idle")

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def OnExit(self, event):
        if self.streamPanel.streamManager.isRecording():
            diag = wx.MessageDialog(None, "Are you sure you want to quit?\nOngoing recordings will not be saved!",
                                    "Ongoing recording detected", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING).ShowModal()
            if diag != wx.ID_YES:
                return
        self.Destroy()

    def OnAbout(self, event):
        wx.MessageBox("This is Xterity v1.2.\nA toolkit to record labstreamlayer streams on the local network.",
                      "emXterity", wx.OK | wx.ICON_INFORMATION)


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None, title="Xterity", size=(1000, 300))
    frame.Show()
    app.MainLoop()
