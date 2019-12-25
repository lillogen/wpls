"""
PHYSEC Online Plotting
"""
# Python libraries
import argparse
# PyQtGraph libraries
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
# Own libraries
from Channel import MeasurementChannel
from worker import Thread, SocketWorker
from colors import kelly_colors as colors
from util import get_channel, timestamp, unit


class Plot(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)

        # Data
        self.channels = list()
        self.scroll = True
        self.start = timestamp()

        # Create window
        window = pg.GraphicsWindow()
        window.setWindowTitle('PHYSEC Online Evaluation')

        # Parse command line, default values provided
        parser = argparse.ArgumentParser(description='Online plotting of PHYSEC measurement data from ZMQ socket.')
        parser.add_argument('-r', dest='address', nargs='+', help='list of remote addresses to subscribe',
                            default='127.0.0.1:6000')
        parser.add_argument('-l', dest='size', help='limit number of measurements per channel to keep in memory',
                            type=int, default=1024)
        parser.add_argument('-s', dest='speed', help='interval in milliseconds to redraw the plot', type=int,
                            default=50)
        parser.add_argument('-m', dest='measure', help='the measurement value to plot', default='rssi')
        self.args = parser.parse_args()

        # Parse addresses
        if isinstance(self.args.address, list):
            addresses = ["tcp://%s" % address for address in self.args.address]
        else:
            addresses = list()
            addresses.append(str("tcp://" + self.args.address))

        # Plot window
        self.measurement_plot = window.addPlot(name='Measurements')
        self.measurement_plot.setLabels(title='Measurements',
                                        left=(self.args.measure.upper(), unit.get(self.args.measure.upper(), '')),
                                        bottom=('Time', unit.get('TIME', '')))
        self.measurement_plot.addLegend()

        # Socket receiving thread
        # Reference to thread is stored for memory reasons on exit
        self.receiver_thread = Thread()
        receive_socket = SocketWorker(addresses, [self.args.measure])
        receive_socket.moveToThread(self.receiver_thread)
        receive_socket.finished.connect(self.receiver_thread.quit)
        receive_socket.measurement_received.connect(self.add_measurement)
        self.receiver_thread.started.connect(receive_socket.receive)
        self.receiver_thread.start()

        # Connect actions and start drawing timer
        self.measurement_plot.scene().sigMouseClicked.connect(self.plot_clicked)
        pg.QtCore.QTimer.singleShot(self.args.speed, self.redraw_plots)

        QtGui.QApplication.instance().exec_()

    def redraw_plots(self):
        """
        Redraws the plots
        """
        # Draw measurements
        for channel in self.channels:
            assert isinstance(channel, MeasurementChannel)
            channel.curve.setData(channel.x(), channel.y(self.args.measure))
        # Finally scroll
        if self.scroll:
            now = timestamp() - self.start
            self.measurement_plot.setXRange(now - 10, now)
        # Set the timer for the next redraw
        pg.QtCore.QTimer.singleShot(self.args.speed, self.redraw_plots)

    @QtCore.pyqtSlot(object)
    def plot_clicked(self, ev):
        """
        Slot when the plot was clicked
        """

        # First we determine which plot was under our click
        
        items = self.measurement_plot.scene().items(ev.scenePos())
        if len(items) > 2 and isinstance(items[-2], pg.PlotItem):
            # Measurement Plot under click
            if items[-2] == self.measurement_plot:
                for item in items:
                    # Legend label was clicked
                    if isinstance(item, pg.LabelItem):
                        for channel in self.channels:
                            if channel.name == item.text:
                                # Toggle visibility and adjust label color (d is default foreground color)
                                channel.toggleVisibility()
                                item.setText(item.text, color={True: 'd', False: '444444'}[channel.visible])
                                break
                        break
                # Some other stuff was clicked
        else:
            if ev.double():
                ## Toggle the automatic scrolling
                #self.scroll = not self.scroll
                print "Storing:", not self.channels[0].storing
                for channel in self.channels:
                    channel.toggleStoring()

    @QtCore.pyqtSlot(str, str, str, float, int, dict)
    def add_measurement(self, fro, to, me, now, sync, meas):
        """
        Receives new measurements and puts them in their channels
        :type meas: dict
        """
        # Put the measurement in its channel
        channel = get_channel(self.channels, fro, to, me, True)
        channel.timestamp.append(now)
        channel.sync.append(sync)
        for name, measurement in meas.iteritems():
            channel.measurements[name].append(measurement)
        # Reduce size if necessary
        channel.reduce(self.args.size)
        # Get a plot if not yet happened
        if channel.curve is None:
            channel.curve = self.measurement_plot.plot(channel.timestamp, channel.measurements[self.args.measure],
                                                       pen=pg.mkPen(width=2,
                                                                    color=colors[len(self.channels) % len(colors)]),
                                                       name=channel.name)


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    evaluate = Plot()
