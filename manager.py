import sys
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import random
import memory
from css import MENU_CSS
import processes
import page_faults

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

        self.thread = page_faults.PageFaultListener()

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
        

        self.createMenuProcesses()

        # set the layout
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.myQMenuBar)    
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def createMenuProcesses(self):
        #### Cria menu
        self.menuProcessStatistics = self.myQMenuBar.addMenu('Estatística de processos')
        # Gráfico: total x usado
        plot1 = QtGui.QAction('&Total x Usado', self)        
        plot1.triggered.connect(lambda: self.plot( memory.plotGraph1() ))
        self.menuProcessStatistics.addAction(plot1)

        # Gráfico: quantidade de processos em cada estado (pronto, suspenso, rodando, etc)
        plot2 = QtGui.QAction('&Processos por estado', self)  
        thread = processes.ProcessStatusListener()      
        plot2.triggered.connect(lambda: self.connectThreadProcesses( thread ))
        self.menuProcessStatistics.addAction(plot2)

    def connectThread(self):
        self.thread = page_faults.PageFaultListener()
        self.thread.start()
        signal = QtCore.SIGNAL("output(PyQt_PyObject)")
        self.connect(self.thread, signal, self.listview)

    def connectThreadProcesses(self, thread):
        self.threadProcesses = thread
        self.threadProcesses.start()
        signal = QtCore.SIGNAL("output(PyQt_PyObject)")
        self.connect(self.threadProcesses, signal, self.plot)
        
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

        
        myPageFaultsQWidget = page_faults.PageFaultsQWidget()
        myPageFaultsQWidget.setTextPID(texts[0])
        myPageFaultsQWidget.setTextCommand(texts[1])
        myPageFaultsQWidget.setTextMinFlt(texts[len(texts)-2])
        myPageFaultsQWidget.setTextMajFlt(texts[len(texts)-1])
        return myPageFaultsQWidget

    def listview(self, data):
        '''show list with page faults'''
        self.threadProcesses.stop()
        if( self.listWidget == None or self.layout.indexOf(self.listWidget) == -1):
            self.listWidget = QtGui.QListWidget()
        else:
            self.listWidget.clear()
        
        for i,text in enumerate(data):
            item = self.formatPsResult(text)

            myQListWidgetItem = QtGui.QListWidgetItem(self.listWidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(item.sizeHint())
            self.listWidget.addItem(myQListWidgetItem)
            self.listWidget.setItemWidget(myQListWidgetItem, item)
            
        self.layout.removeWidget(self.canvas)
        if( self.listWidget != None and self.layout.indexOf(self.listWidget) != -1 and not self.thread.exiting):
            self.listWidget.show()
        else:
            self.layout.addWidget(self.listWidget)

    def plot(self, data):
        ''' plot some random stuff 
            @see: https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt-for-dummies
        '''
        if(len(data[0]) == 2):
            self.threadProcesses.stop()
            print('stop')

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
        print(titles)
        color = ['lightblue', 'green']
        # If the colors are sent
        if(len(data)> 2):
            color = data[2]
        explode = (0.1, 0)  # somente explode primeiro pedaço
        total = sum(titles)
        ax.pie(titles, explode=None, labels=labels, colors=color, autopct=lambda p: '{:.0f}'.format(p * total / 100), shadow=True, startangle=90)


        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())