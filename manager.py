import sys
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import random
import memory
from css import MENU_CSS
import processes

class PageFaultsQWidget (QtGui.QWidget):
    def __init__ (self, parent = None):
        super(PageFaultsQWidget, self).__init__(parent)
        self.label1 = QtGui.QLabel()
        self.label2 = QtGui.QLabel()
        self.label3 = QtGui.QLabel()
        self.label4 = QtGui.QLabel()

        self.vbox = QtGui.QVBoxLayout()

        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addWidget(self.label1, 1, QtCore.Qt.AlignRight)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.label2, 1, QtCore.Qt.AlignRight)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.label3, 1, QtCore.Qt.AlignRight)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.label4 , 1, QtCore.Qt.AlignRight)

        self.vbox.addStretch()
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

    def setTextPID (self, text):
        self.label1.setText(text)

    def setTextCommand (self, text):
        self.label2.setText(text)

    def setTextMinFlt (self, text):
        self.label3.setText(text)

    def setTextMajFlt (self, text):
        self.label4.setText(text)


class Window(QtGui.QDialog):

    listWidget = None
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.listWidget = None

        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.thread = processes.PageFaultListener()

        #### Cria menu
        self.myQMenuBar = QtGui.QMenuBar(self)
        self.myQMenuBar.setStyleSheet(MENU_CSS)
        self.menuMemoria = self.myQMenuBar.addMenu('Memória')
        ##plota grafico 1
        plot1 = QtGui.QAction('&Memória Total x Memória Livre', self)        
        plot1.triggered.connect(lambda: self.plot( memory.plotGraph1() ))
        self.menuMemoria.addAction(plot1)

        ##plota grafico 2
        plot2 = QtGui.QAction('Memória Total x Memória Acessivel', self)        
        plot2.triggered.connect(lambda: self.plot( memory.plotGraph2() ))
        self.menuMemoria.addAction(plot2)
        
        ##plota grafico 3
        plot3 = QtGui.QAction('Memória Total x Memória Cache', self)        
        plot3.triggered.connect(lambda: self.plot( memory.plotGraph3() ))
        self.menuMemoria.addAction(plot3)

        ##plota grafico 4
        plot4 = QtGui.QAction('Swap Total x Memória Total', self)        
        plot4.triggered.connect(lambda: self.plot( memory.plotGraph4() ))
        self.menuMemoria.addAction(plot4)

        ##plota grafico 5
        plot5 = QtGui.QAction('Swap Usado x Swap livre', self)        
        plot5.triggered.connect(lambda: self.plot( memory.plotGraph5() ))
        self.menuMemoria.addAction(plot5)

        ##plota grafico 5
        plot6 = QtGui.QAction('Faltas de páginas por processos', self)
        plot6.triggered.connect(self.connectThread)        
        self.menuMemoria.addAction(plot6)
        

        # set the layout
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.myQMenuBar)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def connectThread(self):
        self.thread = processes.PageFaultListener()
        self.thread.start()
        print('cc')
        signal = QtCore.SIGNAL("output(PyQt_PyObject)")
        self.connect(self.thread, signal, self.listview)
        
    def formatPsResult(self, line):
        """ Format each line result from the ps command

        @param line Line from ps command
        @return 
        """
        #separate the values
        texts = line.split()

        items = []
        ## format process name
        texts[1] = ' '.join(texts[1:len(texts)-2]).ljust(50)

        
        myPageFaultsQWidget = PageFaultsQWidget()
        myPageFaultsQWidget.setTextPID(texts[0])
        myPageFaultsQWidget.setTextCommand(texts[1])
        myPageFaultsQWidget.setTextMinFlt(texts[len(texts)-2])
        myPageFaultsQWidget.setTextMajFlt(texts[len(texts)-1])
        return myPageFaultsQWidget

    def listview(self, data):
        '''show list with page faults'''

        if( self.listWidget == None or self.layout.indexOf(self.listWidget) == -1):
            self.listWidget = QtGui.QListWidget()
        else:
            self.listWidget.clear()
        
        for i,text in enumerate(data):
            line = self.formatPsResult(text)
            #print(line)
            """
            # Create PageFaultsQWidget
            myPageFaultsQWidget = QtGui.QLabel()
            myPageFaultsQWidget.setText(line)
            # Create QListWidgetItem"""
            myQListWidgetItem = QtGui.QListWidgetItem(self.listWidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(line.sizeHint())
            self.listWidget.addItem(myQListWidgetItem)
            self.listWidget.setItemWidget(myQListWidgetItem, line)
            #self.listWidget.insertItem(i, line)
            #myQListWidgetItem.setLayout(line)
            #self.listWidget.addItem(myQListWidgetItem)
            #myQListWidgetItem.deleteLater()
            
        self.layout.removeWidget(self.canvas)
        if( self.listWidget != None and self.layout.indexOf(self.listWidget) != -1 and not self.thread.exiting):
            self.listWidget.show()
        else:
            print("dd")
            self.layout.addWidget(self.listWidget)

    def plot(self, data):
        ''' plot some random stuff 
            @see: https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt-for-dummies
        '''
        print('ee')
        self.thread.stop()
        if( self.listWidget != None):
            self.listWidget.hide()
            self.layout.addWidget(self.canvas)

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data 
        labels = data[0]
        titles = data[1]
        color = ['lightblue', 'green']
        explode = (0.1, 0)  # somente explode primeiro pedaço
        total = sum(titles)
        ax.pie(titles, explode=explode, labels=labels, colors=color, autopct=lambda p: '{:.0f}'.format(p * total / 100), shadow=True, startangle=90)


        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())