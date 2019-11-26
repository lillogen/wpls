from pyqtgraph.Qt import QtCore
from Channel import ProcessingChannel


class MeasurementWorker(QtCore.QObject):
    # Qt Signals
    finished = QtCore.pyqtSignal()
    processed = QtCore.pyqtSignal(list)

    def __init__(self, module, queue):
        QtCore.QObject.__init__(self)
        self.module = module
        self.queue = queue
        self.channels = list()

    def max_mutual_sync(self):
        """
        Gets the maximum sync that is available in all channels
        :return:
        """
        max_sync = -1
        for channel in self.channels:
            assert isinstance(channel, ProcessingChannel)
            # Skip sniffer
            if channel.is_sniffer():
                continue
            if max_sync == -1 or max(channel.sync) < max_sync:
                max_sync = max(channel.sync)
        return max_sync

    def processing_copy(self, synchronize = True):
        """
        Creates a copy of the channel data with size specified in the modules block size
        :param synchronize: True if channels should be synchronized
        :return: the channel copy
        """
        result = list()
        # Greatest mutual sync
        max_sync = self.max_mutual_sync()
        # Loop over all channels and remove extra data
        for channel in self.channels:
            # Prepare the data copy
            assert isinstance(channel, ProcessingChannel)
            new_channel = ProcessingChannel(channel.fro, channel.to, channel.me)
            new_channel.timestamp = channel.timestamp
            # Iterate backwards over channel data
            for index in xrange(len(channel) - 1, -1, -1):
                # Only copy as long as the block is not full
                if len(new_channel) >= self.module.block_size:
                    break
                # Skip higher syncs
                if synchronize and channel.sync[index] > max_sync:
                    continue
                # Skip duplicates. We only keep the newest
                if synchronize and channel.sync[index] in new_channel.sync:
                    continue
                # Copy sync
                new_channel.sync.append(channel.sync[index])
                # Copy measurements
                for name in channel.measurements.keys():
                    new_channel.measurements[name].append(channel.measurements[name][index])
            # Reverse the items for correct order
            new_channel.sync.reverse()
            for name in new_channel.measurements.keys():
                new_channel.measurements[name].reverse()
            result.append(new_channel)
        return result

    def process(self):
        """
        Worker method
        """
        while True:
            # Wait for data
            data = self.queue.get()
            # Get a channel
            for candidate in self.channels:
                assert isinstance(candidate, ProcessingChannel)
                if candidate.fro == data[0] and candidate.to == data[1] and candidate.me == data[2]:
                    channel = candidate
                    break
            else:
                channel = ProcessingChannel(data[0], data[1], data[2])
                self.channels.append(channel)
            # Set the data
            channel.timestamp.append(data[3])
            channel.sync.append(data[4])
            for name, value in data[5].iteritems():
                channel.measurements[name].append(value)
            channel.new += 1
            # Check if we can process yet
            if min(map(lambda channel: channel.new, self.channels)) >= self.module.refresh:
                # Prepare data
                channels_copy = self.processing_copy(self.module.synchronize)
                # Check for correct block size
                abort = False
                for channel_copy in channels_copy:
                    assert isinstance(channel_copy, ProcessingChannel)
                    if not channel_copy.is_sniffer() and len(channel_copy) < self.module.block_size:
                        abort = True
                        break
                if abort:
                    continue
                # Do processing
                result = self.module.process(channels_copy)
                self.processed.emit(result)
                # Reduce size
                for channel in self.channels:
                    del channel.timestamp[:self.module.refresh]
                    del channel.sync[:self.module.refresh]
                    del channel.measurements[:self.module.refresh]
                # Reset process counter
                for channel in self.channels:
                    channel.new = 0

        self.finished.emit()
