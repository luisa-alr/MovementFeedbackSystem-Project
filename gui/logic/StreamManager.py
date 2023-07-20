from pylsl import ContinuousResolver, StreamInlet, resolve_byprop, local_clock
from threading import Thread, get_ident
from datetime import datetime
import time
import ntpath
from logic.helpers import prettyPrintFormat
from logic.helpers import slugify
from logic.io.PicklePersistenceLayer import PicklePersistenceLayer


class StreamManager:

    def __init__(self):
        self.resolver = ContinuousResolver()
        self.inlets = []
        self.recordingThreads = []
        self.pathname = "."
        self.filename = "recording"
        self.timehash = int(time.time())

    def isRecording(self):
        return len(self.recordingThreads) > 0

    def checkStreamAvailability(self):
        return self.resolver.results()

    def connectStreams(self, source_ids):
        #disconnect all other streams
        self.inlets = []
        doubleSourceId = False
        #connect to streams given their uids
        for (rowid, source_id) in source_ids:
            stream = resolve_byprop('source_id', source_id, timeout=20.0)
            if len(stream) > 0:
                inlet = StreamInlet(stream[0])
                time_correction = inlet.time_correction()
                self.inlets.append((rowid, inlet, time_correction))
                if len(stream) > 1:
                    doubleSourceId = True
        return len(self.inlets) == len(source_ids), doubleSourceId, self.inlets

    def startRecordingFromStreams(self, pathname, persistenceDuration):
        self.pathname, self.filename = ntpath.split(pathname)
        self.filename = slugify(self.filename)
        self.timeLastRecording = local_clock()
        self.startDateOfRecording = str(datetime.now())
        self.timehash = int(time.time())
        #start a recording thread for every stream
        for inlet in self.inlets:
            recordThread = RecordThread(inlet[1], self.pathname, self.filename, self.timehash, persistenceDuration)
            self.recordingThreads.append(recordThread)
            recordThread.start()
        return self.inlets

    def stopRecordingFromStreams(self):

        #stop all recording threads
        for thread in self.recordingThreads:
            thread.running = False
            thread.join()

        #recording summary
        durationRecording = local_clock() - self.timeLastRecording
        file = open(self.pathname + "/" + slugify(self.filename) + "_" + str(self.timehash) + ".txt", 'w')
        file.write("Start of recording: " + self.startDateOfRecording + "\n")
        file.write("End of recording: " + str(datetime.now()) + "\n")
        file.write("Duration of recording (LSL measured): " + str(durationRecording) + " (ca. " + "{0:.1f}".format(durationRecording/60.0) + " min)\n")
        file.write("Streams:\n")
        file.write("name\ttype\tchannel_count\tsample_rate\tformat\thost\tuid\ttime_correction\tsource_id\tversion\tcreated_at\tsample_count\n")
        streamResults = []

        #save return data
        for thread in self.recordingThreads:
            info = thread.inlet.info()
            file.write(str(info.name()) + "\t" + str(info.type()) + "\t" + str(info.channel_count()) + "\t" + str("Irregular" if info.nominal_srate() == 0.0 else str(info.nominal_srate())) + "\t" + prettyPrintFormat(info.channel_format()) + "\t" + str(info.hostname()) + "\t"
                       + str(info.uid()) + "\t" + str(thread.timeCorrection) + "\t" + str(info.source_id()) + "\t" + str(info.version()) + "\t" + str(info.created_at()) + "\t" + str(thread.persistenceLayer.getDataCount()) + "\n")

            if info.nominal_srate() == 0.0:
                streamResults.append((str(info.name()), str(thread.persistenceLayer.getDataCount()) + " entries"))
            else:
                streamResults.append((str(info.name()), "{0:.1f}".format(thread.persistenceLayer.getDataCount()/info.nominal_srate()) + "s"))
        self.recordingThreads = []
        return durationRecording, streamResults



class RecordThread(Thread):

    def __init__(self, inlet, pathname, fileName, timehash, persistenceDuration):
        Thread.__init__(self, daemon=True)
        self.running=False
        self.inlet = inlet
        self.timeCorrection = inlet.time_correction()
        self.persistenceLayer = PicklePersistenceLayer(pathname, fileName, str(self.inlet.info().source_id()), str(self.inlet.info().name()), timehash, persistenceDuration)

    def run(self):
        self.running=True
        self.inlet.open_stream(timeout=10.0)
        while self.running:
            sample, ts = self.inlet.pull_sample(timeout=1.0)
            if ts is not None:
                ts += self.timeCorrection
                self.persistenceLayer.appendDatum(ts, sample)
        self.inlet.close_stream()
        self.persistenceLayer.close()