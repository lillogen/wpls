import zmq
from pyqtgraph.Qt import QtCore
from struct import unpack
from binascii import unhexlify
from util import timestamp


class SocketWorker(QtCore.QObject):
    # Qt Signals
    finished = QtCore.pyqtSignal()
    measurement_received = QtCore.pyqtSignal(str, str, str, float, int, dict)

    def __init__(self, addresses, measures=['rssi']):
        QtCore.QObject.__init__(self)
        self.start = timestamp()
        self.addresses = addresses
        self.measures = measures
        self.seq = dict()

    @QtCore.pyqtSlot()
    def receive(self):
        # ZMQ socket
        context = zmq.Context()
        data_socket = context.socket(zmq.SUB)
        for address in self.addresses:
            data_socket.connect(address)
        data_socket.setsockopt(zmq.SUBSCRIBE, "")
        while True:
            recv = data_socket.recv()
            now = timestamp() - self.start
            message = parse_socket_message(recv)

            # Skip weird sniffed stuff
            if message['to'] != message['me']:
                # Checksum correct
                if int(message['aux']) & 0x02 == 0:
                    continue

                # Sniffed measurement packet
                elif len(message['payload']) == 52:
                    seq = message['payload'][4:6]
                    message['payload'] = str(unpack('<L', unhexlify(message['payload'][44:]))[0])
                    self.seq[(seq, message['me'])] = (message['to'], message['from'], message['payload'])

                # Parse an ACK
                elif message['from'] == '0000000000000000' or message['to'] == '0000000000000000':
                    params = self.seq.get((message['payload'][4:6], message['me']), list())
                    if len(params) == 3:
                        del self.seq[(message['payload'][4:6], message['me'])]
                        message['from'] = params[0]
                        message['to'] = params[1]
                        message['payload'] = params[2]
                    else:
                        continue

                # Some other weird sniffed stuff
                else:
                    continue

            # Parse measurements
            measurements = dict()
            for measure in self.measures:
                measurements[measure] = int(message.get(measure, '0'))
            # Put the measurement in its channel
            self.measurement_received.emit(message['from'], message['to'], message['me'], now, int(message['payload']),
                                           measurements)
        self.finished.emit()


def parse_socket_message(message):
    """
    Parse a ZMQ message into a dictionary
    :param message: The ZMQ message to be parsed
    :rtype: dict()
    :return: A dictionary containing the message
    """
    parsed = dict()
    for commaSplit in message.split(';'):
        split = commaSplit.split('=')
        if len(split) == 2:
            parsed[split[0]] = split[1]
        else:
            print 'Invalid message %s' % message
            return dict()
    return parsed
