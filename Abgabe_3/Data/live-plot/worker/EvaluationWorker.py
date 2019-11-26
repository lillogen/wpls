from pyqtgraph.Qt import QtCore


# Not yet used due to some weird fault that freezes the app
class EvaluationWorker(QtCore.QObject):
    # Qt Signals
    finished = QtCore.pyqtSignal()
    evaluated = QtCore.pyqtSignal(list)

    def __init__(self, function, data):
        QtCore.QObject.__init__(self)
        self.function = function
        self.data = data

    def evaluate(self):
        result = self.function(self.data)
        self.evaluated.emit(result)
        self.finished.emit()
