from logic.io.PersistenceLayer import PersistenceLayer
import pickle



class PicklePersistenceLayer(PersistenceLayer):

    def __init__(self, pathname, filename, streamSource, streamName, timehash, persistenceDuration):
        PersistenceLayer.__init__(self, pathname, filename, streamSource, streamName, timehash, persistenceDuration)
        self.pickleFile = open(self.pathname + "/" + self.filename + "_" + self.streamName + "_" + self.streamSource +  str(self.timehash) + ".p",'wb')


    def storeData(self):
        pickle.dump(self.data, self.pickleFile)
        self.pickleFile.flush()
        self.data = []

    def close(self):
        if len(self.data) != 0:
            self.storeData()
        self.pickleFile.close()
