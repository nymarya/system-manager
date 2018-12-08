from PyQt4 import QtGui, QtCore

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
