import wx
import os
from time import gmtime, strftime
from threading import Thread
from pylsl import StreamOutlet, StreamInfo, IRREGULAR_RATE

class MarkerStream(wx.Frame):

    def __init__(self, parent, title):
        super(MarkerStream, self).__init__(parent, title=title)

        self.panel_one = MarkerInputPanel(self)
        self.panel_two = MarkerButtonsPanel(self, [])
        self.panel_two.Hide()

        self.lsl_stream = LSLSendStringMarkers()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        self.sizer.Add(self.panel_two, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        #self.CreateStatusBar()

        self.Centre()
        self.Show()
        self.Fit()

    def onGenerateMarkers(self, event):
        if self.panel_one.IsShown():
            self.SetTitle("Send Markers")
            self.panel_one.Hide()
            markers = [self.panel_one.markersInput.GetLineText(i) for i in range(0, self.panel_one.markersInput.GetNumberOfLines())]
            self.panel_two = MarkerButtonsPanel(self, markers)
            self.panel_two.Show()
        else:
            self.SetTitle("Specify Markers")
            self.panel_one.Show()
            self.panel_two.Hide()
        self.Layout()

    def onSendMarker(self, event):
        Thread(target=self.lsl_stream.sendStringMarker, args=(event.GetEventObject().GetName(), )).start()

class MarkerInputPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        markersText = wx.StaticText(self, wx.ID_ANY, "Marker")
        hbox.Add(markersText, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.markersInput = wx.TextCtrl(self, size=(200, 100), style=wx.TE_MULTILINE)
        hbox.Add(self.markersInput, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(hbox)

        self.button_generateMarkers = wx.Button(self, label="Generate Marker Buttons")
        self.button_generateMarkers.Bind(wx.EVT_BUTTON, parent.onGenerateMarkers)
        vbox.Add(self.button_generateMarkers, 0, wx.ALIGN_CENTER, 5)
        self.SetSizer(vbox)

class MarkerButtonsPanel(wx.Panel):

    def __init__(self, parent, markerList):
        wx.Panel.__init__(self, parent=parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        acceleratorIndex=0
        for marker in markerList:
            markerButton = wx.Button(self, label="&" + str(acceleratorIndex) + ":  " + marker, style=wx.BU_LEFT, name=marker)
            markerButton.Bind(wx.EVT_BUTTON, parent.onSendMarker)

            #bind to ACC_KEY if < 10
            #if acceleratorIndex < 10:
            #    randomId = wx.NewId()
            #    self.Bind(wx.EVT_MENU, parent.onSendMarker, id=randomId)
            #    accelTable = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord(str(acceleratorIndex), randomId))])
            #    self.SetAcceleratorTable(accelTable)
            vbox.Add(markerButton, 0, wx.ALIGN_CENTER)
            acceleratorIndex +=1

        self.SetSizer(vbox)
        self.Fit()

class LSLSendStringMarkers():

    def __init__(self):
        info = StreamInfo(name='CustomMarkerStream', type='Markers', channel_count=1, nominal_srate=IRREGULAR_RATE,
                               channel_format='string', source_id='' + os.environ['HOME'] + '-custom_marker_stream-' + strftime("%Y-%m-%d_%H-%M-%S", gmtime()))
        self.outlet = StreamOutlet(info)

    def sendStringMarker(self, marker):
        self.outlet.push_sample([marker])

if __name__ == '__main__':
    app = wx.App()
    MarkerStream(None, title="Marker Stream")
    app.MainLoop()



