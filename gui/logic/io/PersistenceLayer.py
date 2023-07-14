import time
from logic.helpers import slugify


class PersistenceLayer:

    def __init__(self, pathname, filename, streamSource, streamName, timehash, persistenceDuration):
        self.data = []
        self.dataCounter=0
        self.pathname = pathname
        self.filename = slugify(filename)
        self.streamSource = slugify(streamSource)
        self.streamName = slugify(streamName)
        self.timehash = timehash
        self.persistenceDuration = persistenceDuration
        self.lastTime = time.time()

    def appendDatum(self, timestamp, data):
        self.data.append((timestamp, data))
        self.dataCounter = self.dataCounter+1
        if (time.time() - self.lastTime) > self.persistenceDuration:
            self.storeData()
            self.lastTime = time.time()

    '''
    should be fast, otherwise consider threading; make sure self.data is handled threadsafe!
    '''
    def storeData(self):
        pass

    '''
    flush and close persistence layer. Return number of collected samples
    '''
    def close(self):
        pass

    def getDataCount(self):
        return self.dataCounter
