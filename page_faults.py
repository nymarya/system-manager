from PyQt4 import QtGui, QtCore
from time import sleep
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import subprocess

class PageFaultsQWidget (QtGui.QWidget):
    """ QWidget that defines a item at the the list
    of page faults.
    """

    def __init__ (self, parent = None):
        super(PageFaultsQWidget, self).__init__(parent)
        # Init labels
        self.labelPID = QtGui.QLabel()
        self.labelCommand = QtGui.QLabel()
        self.labelMinFlt = QtGui.QLabel()
        self.labelMajFlt = QtGui.QLabel()

        # Adjust labels at the layout of a item
        self.vbox = QtGui.QVBoxLayout()
        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addWidget(self.labelPID, 1, QtCore.Qt.AlignRight)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.labelCommand, 1, QtCore.Qt.AlignRight)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.labelMinFlt, 1, QtCore.Qt.AlignRight)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.labelMajFlt , 1, QtCore.Qt.AlignRight)

        self.vbox.addStretch()
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

    def setTextPID (self, text):
        self.labelPID.setText(text)

    def setTextCommand (self, text):
        self.labelCommand.setText(text)

    def setTextMinFlt (self, text):
        self.labelMinFlt.setText(text)

    def setTextMajFlt (self, text):
        self.labelMajFlt.setText(text)


class PageFaultListener(QtCore.QThread):

    def __init__(self, parent = None):
    
        QtCore.QThread.__init__(self, parent)
        self.exiting = False

    def __del__(self):

        self.exiting = True
        self.wait()

    def render(self):
        self.start()
    
    def stop(self):
        self.exiting = True
        self.__del__()


    def run(self):
        """ Thread receive the message and send the position of the
            components to the GUI
        """
        while not self.exiting:
            subprocess.call(["ps -eo pid,command,min_flt,maj_flt --sort=-maj_flt,-min_flt > pageFaults.txt"], shell=True)
            # abre arquivo com informacoes
            arc = open('pageFaults.txt', 'r')
            # le cada linha do arquivo
            text = arc.readlines()
            # fecha arquivo
            arc.close()
            self.emit(SIGNAL("output(PyQt_PyObject)"),text)
            
            sleep(1)
