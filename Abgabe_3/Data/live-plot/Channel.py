from DictList import DictList


class Channel:
    def __init__(self, fro, to, me, store_file=True, basepath=None):
        """
        Construct a channel
        :param fro: from address
        :param to: to address
        :param me: receiver's address
        """
        self.fro = fro
        self.to = to
        self.me = me
        self.timestamp = list()
        self.sync = list()
        self.measurements = DictList()
        self.name = "%s > %s , %s" % (fro[-4:], to[-4:], me[-4:])
        self.store_file = store_file
        if store_file:
            self.storing = False
            from os import getcwd, path, makedirs
            if not basepath:
                basepath = path.join(getcwd(), 'output')
            try:
                makedirs(basepath)
            except:
                pass
            self.fp = open(path.join(basepath, "%s_%s_%s.csv"%(fro, to, me)), 'w+')
        else:
            self.storing = False
            self.fp = None
        
    def is_sniffer(self):
        return self.to != self.me
    
    def toggleStoring(self):
        self.storing = not self.storing
    
    def reduce(self, max_size):
        # If we reached the max size, we delete the first elements in our lists
        if len(self) > max_size:
            if self.store_file and self.storing:
                self.fp.write(str(self.sync[0]) + ";" + str(self.measurements._data.values()[0][0]) + "\n")        
                self.fp.flush()
            del self.sync[0]
            del self.measurements[0]

    def __len__(self):
        return len(self.sync)

    def __repr__(self):
        return str("%s with %d items" % (self.me, len(self.measurements._data.values()[0])))

    def __del__(self):
        if self.store_file:
            if self.storing:
                for s, m in zip(self.sync, self.measurements._data.values()[0]):
                    self.fp.write(str(s) + ";" + str(m) + "\n")
            self.fp.close()


class ProcessingChannel(Channel):
    def __init__(self, fro, to, me):
        """
        Construct a channel for processing data.
        It is based on the Channel class but provides an extra timestamp value for usage as x-coordinate.
        This allows to arrange processing results near used measurement data
        :param fro: from address
        :param to: to address
        :param me: receiver's address
        """
        Channel.__init__(self, fro, to, me)
        self.new = 0


class PlotChannel:
    def __init__(self):
        self.visible = True

    def toggleVisibility(self):
        self.visible = not self.visible

    def x(self):
        raise NotImplemented

    def y(self):
        raise NotImplemented


class MeasurementChannel(Channel, PlotChannel):
    def __init__(self, fro, to, me):
        Channel.__init__(self, fro, to, me)
        PlotChannel.__init__(self)
        self.new = 0
        self.curve = None

    def x(self):
        if self.visible:
            return self.timestamp
        return []

    def y(self):
        return self.y(self.measurements.keys()[0])

    def y(self, field):
        if self.visible:
            return self.measurements[field]
        return []

    def reduce(self, max_size):
        Channel.reduce(self, max_size)
        # Also reduce the timestamp list
        if len(self.timestamp) > max_size:
            del self.timestamp[0]


class EvaluationChannel(PlotChannel):
    def __init__(self, index, name):
        """
        Creates a EvaluationChannel instance
        :param index: index identifying the plot
        :param name: name of the graph used in legend
        """
        PlotChannel.__init__(self)
        self.index = index
        self.name = name
        self._x = list()
        self._y = list()
        self.curve = None

    def x(self):
        if self.visible:
            return self._x
        return []

    def y(self):
        if self.visible:
            return self._y
        return []

    def clear(self):
        self._x = list()
        self._y = list()
