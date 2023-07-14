import wx
import wx.grid
from logic.StreamManager import StreamManager
from threading import Thread
from logic.helpers import prettyPrintFormat
from wx.lib.intctrl import IntCtrl


headers = ["Stream", "Type", "#Channels", "SampleRate", "Format", "Hosted on", "Source id", "Time offset", "Status"]

class StreamOverviewPanel(wx.Panel):

    def __init__(self, parent):
        super(StreamOverviewPanel, self).__init__(parent)
        self.parent = parent
        self.streamManager = StreamManager()

        self.grid = wx.grid.Grid(self)
        self.grid.EnableEditing(False)
        self.grid.CreateGrid(0,len(headers))
        for i in range(0, len(headers)):
            self.grid.SetColLabelValue(i, headers[i])
        self.grid.SetColFormatNumber(3)
        self.grid.SetColFormatNumber(4)
        self.grid.SetColFormatNumber(5)
        self.grid.SetColFormatFloat(8)

        szr = wx.BoxSizer(wx.VERTICAL)
        szr.Add(self.grid, flag=wx.EXPAND, proportion=1)

        #control buttons
        szr.Add((-1, 10))
        szr.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_checkStreams = wx.Button(self, label="Check Streams")
        self.btn_checkStreams.Bind(wx.EVT_BUTTON, self.onCheckStreams)
        hbox2.Add(self.btn_checkStreams, border=5)

        self.btn_connectStreams = wx.Button(self, label="Connect Streams")
        self.btn_connectStreams.Bind(wx.EVT_BUTTON, self.onConnectStreams)
        self.btn_connectStreams.Enable(False)
        hbox2.Add(self.btn_connectStreams, border=5)
        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.onGridSelect)

        self.btn_recordStreams = wx.Button(self, label="Record Streams")
        self.btn_recordStreams.Bind(wx.EVT_BUTTON, self.onRecordStreams)
        self.btn_recordStreams.Enable(False)
        hbox2.Add(self.btn_recordStreams, border=5)

        szr.Add(hbox2, flag= wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=5)

        #persistence duration
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        st_persistenceDuration = wx.StaticText(self, label="Persistence in sec:")
        hbox3.Add(st_persistenceDuration, flag=wx.RIGHT | wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=10)
        self.tc_persistence = IntCtrl(self, value=10, min=0, max=36000, size=(50, -1)) 
        hbox3.Add(self.tc_persistence, flag=wx.ALIGN_CENTER_VERTICAL)
        szr.Add(hbox3, flag=wx.EXPAND | wx.LEFT, border=5)

        self.SetSizer(szr)

    def onRecordStreams(self, e):
        if self.streamManager.isRecording():
            self.parent.SetStatusText("Stopping recording and writing data...")
            StopRecordingFromStreams(self)

        else:
            self.startRecordingStreams()


    def onGridSelect(self, e):
        self.btn_connectStreams.Enable(not self.streamManager.isRecording() and len(self.grid.GetSelectedRows()) > 0)

    def onCheckStreams(self, e):
        self.parent.SetStatusText("Looking for streams...")
        self.updateStreams()
        self.parent.SetStatusText("Idle")

    def onConnectStreams(self, e):
        self.parent.SetStatusText("Connecting to streams...")
        ConnectStreamsTask(self)


    def updateStreams(self):
        self.grid.ClearGrid()
        while self.grid.GetNumberRows() > 0:
            self.grid.DeleteRows()
        streams = self.streamManager.checkStreamAvailability()
        for streamInfo in streams:
            self.grid.InsertRows()
            self.grid.SetCellValue(0, 0, streamInfo.name())
            self.grid.SetCellValue(0, 1, streamInfo.type())
            self.grid.SetCellValue(0, 2, str(streamInfo.channel_count()))
            self.grid.SetCellValue(0, 3, str("Irregular" if streamInfo.nominal_srate() == 0.0 else str(streamInfo.nominal_srate())))
            self.grid.SetCellValue(0, 4, prettyPrintFormat(streamInfo.channel_format()))
            self.grid.SetCellValue(0, 5, streamInfo.hostname())
            if streamInfo.source_id() == "":
                self.grid.SetCellBackgroundColour(0, 6, wx.Colour( 255, 0, 0 ))
            else:
                self.grid.SetCellValue(0, 6, streamInfo.source_id())
            self.grid.SetCellValue(0, 7, "N/A")
            self.grid.SetCellValue(0, 8, "Disconnected")
        self.grid.AutoSize()

    def connectToStreams(self):
        source_ids = []
        for i in self.grid.GetSelectedRows():
            source_ids.append((i, self.grid.GetCellValue(i, 6)))
        allFound, doubleSourceIds, streams = self.streamManager.connectStreams(source_ids)
        for i in range(0, self.grid.GetNumberRows()):
            self.grid.SetCellValue(i, 7, "N/A")
            self.grid.SetCellValue(i, 8, "Disconnected")

        for (rowid, inlets, timeCorrection) in streams:
            self.grid.SetCellValue(rowid, 7, str(timeCorrection))
            self.grid.SetCellValue(rowid, 8, "Connected")

        self.grid.AutoSize()
        return allFound, doubleSourceIds

    def startRecordingStreams(self):

        if not self.tc_persistence.IsInBounds():
            dial = wx.MessageDialog(None, 'Persistence period must be within 0 and 36000 (10 hours).',
                                    'Error', wx.OK | wx.ICON_ERROR)
            dial.ShowModal()
            return

        with wx.FileDialog(self, "Choose recording name",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            recordingStreams = self.streamManager.startRecordingFromStreams(pathname, self.tc_persistence.GetValue())
            for (rowid, inlets, timeCorrection) in recordingStreams:
                self.grid.SetCellValue(rowid, 8, "Recording")
            self.btn_recordStreams.SetLabel("Stop recording")
            self.btn_connectStreams.Enable(False)
            self.btn_checkStreams.Enable(False)
            self.tc_persistence.Enable(False)
            self.parent.SetStatusText("Recording ...")

    def stopRecordingStreams(self):
        durationRecording, streamResults = self.streamManager.stopRecordingFromStreams()

        stringStreamResults = ""
        for stream in streamResults:
            stringStreamResults += stream[0] + ": " + str(stream[1] + "\n")

        wx.MessageDialog(None, 'Duration: ' + "{0:.1f}".format(durationRecording) + "s (" + "{0:.1f}".format(durationRecording/60.0) + 'min)\n\n' +
                         stringStreamResults, 'Recording complete', wx.ICON_INFORMATION | wx.OK | wx.CENTRE).ShowModal()


class ConnectStreamsTask(Thread):
    def __init__(self, panel):
        Thread.__init__(self)
        self.panel = panel
        self.start()

    def run(self):
        allFound, doubleSourceIds = self.panel.connectToStreams()
        if not allFound:
            dial = wx.MessageDialog(None, 'Failed to connect to at least one specified Stream.\nCheck connection and repeat.',
                                    'Error', wx.OK | wx.ICON_ERROR)
            dial.ShowModal()
        if doubleSourceIds:
            dial = wx.MessageDialog(None, 'Found at least two streams for a specified source id.\nSource ids should uniquely identify a stream.\nOnly the first found stream will be recorded (not necessarily the selected one)', 'Detected multiple identical source_id', wx.OK | wx.ICON_WARNING)
            dial.ShowModal()
        self.panel.parent.SetStatusText("Idle")
        if allFound:
            self.panel.btn_recordStreams.Enable(True)


class StopRecordingFromStreams(Thread):
    def __init__(self, panel):
        Thread.__init__(self)
        self.panel = panel
        self.start()

    def run(self):
        self.panel.stopRecordingStreams()
        self.panel.parent.SetStatusText("Idle")
        self.panel.btn_recordStreams.SetLabel("Record Streams")
        self.panel.btn_recordStreams.Enable(False)
        self.panel.btn_connectStreams.Enable(False)
        self.panel.btn_checkStreams.Enable(True)
        self.panel.tc_persistence.Enable(True)
        # check for streams to make sure we initialize them properly again
        self.panel.updateStreams()

