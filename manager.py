import sys
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from PyQt4.QtGui import * 
from PyQt4.QtCore import * 

import random
import memory
import managerProcesses
from css import MENU_CSS
import processes
import page_faults

from functools import partial


class Window(QtGui.QDialog):


    listWidget = None


    man = managerProcesses.ManagerProcesses()

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.listWidget = None

        self.table = None
        self.tableItem = None



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


        self.menuProcess = self.myQMenuBar.addMenu('Processo')
     

        plot7 = QtGui.QAction('&Listar processos ativos', self)        
        plot7.triggered.connect(lambda: self.listviewProc( self.man.listProcesses() ))
        self.menuProcess.addAction(plot7)

        plot8 = QtGui.QAction('&Processador total x Processador usado', self)        
        plot8.triggered.connect(lambda: self.plot( memory.plotGraph5() ))
        self.menuProcess.addAction(plot8)

        plot9 = QtGui.QAction('&Processos em cada estado no processador', self)        
        plot9.triggered.connect(lambda: self.plot( memory.plotGraph5() ))
        self.menuProcess.addAction(plot9)


        self.generateReport = self.myQMenuBar.addMenu('Gerar relatório')


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
        thread = processes.CPUListener
        plot1.triggered.connect(lambda: self.connectThreadProcesses( thread ))
        self.menuProcessStatistics.addAction(plot1)

        # Gráfico: quantidade de processos em cada estado (pronto, suspenso, rodando, etc)
        plot2 = QtGui.QAction('&Processos por estado', self)  
        thread1 = processes.ProcessStatusListener      
        plot2.triggered.connect(lambda: self.connectThreadProcesses( thread1 ))
        self.menuProcessStatistics.addAction(plot2)

    def connectThread(self):
        self.thread = page_faults.PageFaultListener()
        self.thread.start()
        signal = QtCore.SIGNAL("output(PyQt_PyObject)")
        self.connect(self.thread, signal, self.listview)

    def connectThreadProcesses(self, thread):
        try:
            self.threadProcesses.stop()
        except:
            pass
        self.threadProcesses = thread()
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


    def listviewProc(self, data):

        self.processesData = data


        # busca por PID
        inputSearch = QLineEdit()
        inputSearch.setFixedWidth(200)
        
        btnSearch = QtGui.QPushButton("Buscar")
        btnSearch.setFixedWidth(80)

        btnSearch.clicked.connect( lambda: self.man.searchProcess( inputSearch ) )


        self.layout.addWidget(inputSearch)
        self.layout.addWidget(btnSearch)

      
        # inicio config tabela
        if( self.table == None or self.layout.indexOf(self.table) == -1):
            self.table = QtGui.QTableWidget()
        else:
            self.table.clear()



        self.tableItem 	= QTableWidgetItem()
    
        # initiate table
        self.table.setWindowTitle("Gerenciador de processos")
        self.table.setRowCount(len(data))
        self.table.setColumnCount(6)
        
        


        for i,text in enumerate(data):

            txtSplit = " ".join(text.split()) 
            words = txtSplit.split(" ")
            user = words[0]
            pid = words[1]

            command = text
            command = command.replace(user, '')
            command = command.replace(pid, '')
        
            self.table.setItem(i,0, QTableWidgetItem(user))
            self.table.setItem(i,1, QTableWidgetItem(pid))
            self.table.setItem(i,2, QTableWidgetItem(command))
            

            # kill button
            buttonKill = QtGui.QPushButton("Kill")
            self.table.setCellWidget(i,3, buttonKill)
            buttonKill.clicked.connect(partial(self.man.killProcess, pid, command, i))

            # more info button
            buttonInfos = QtGui.QPushButton("Infos")
            self.table.setCellWidget(i,4, buttonInfos)
            buttonInfos.clicked.connect(partial(self.man.infoProcess, pid, command, i))

            # tree button
            buttonTree = QtGui.QPushButton("Árvore")
            self.table.setCellWidget(i,5, buttonTree)
            buttonTree.clicked.connect(partial(self.man.treeProcess, pid, command, i))

            

        # show table
        self.layout.addWidget(self.table)
        self.layout.removeWidget(self.canvas)




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
        # Para a thread de processos se o dado recebido não for float (CPU)
        # Ou se receber for mais de 2 objetos (Status)
        if( not isinstance(data[0], float) and len(data[0]) == 2 and hasattr(self, 'threadProcesses')):
            self.threadProcesses.stop()

        self.thread.stop()
        if( self.listWidget != None):
            self.listWidget.hide()
            self.layout.addWidget(self.canvas)

        if(hasattr(self, 'threadProcesses') and self.threadProcesses.isCPU):
            self.plotCPU(data)
        else:
            self.plotData(data)

        # refresh canvas
        self.canvas.draw()

    def plotData(self, data):

        for ax in self.figure.axes:
            self.figure.delaxes(ax)
        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data 
        labels = data[0]
        titles = data[1]
        
        color = ['lightblue', 'green']
        # If the colors are sent
        if(len(data)> 2):
            color = data[2]
        explode = (0.1, 0)  # somente explode primeiro pedaço
        total = sum(titles)
        ax.pie(titles, explode=None, labels=labels, colors=color, autopct=lambda p: '{:.0f}'.format(p * total / 100), shadow=True, startangle=90)


    def plotCPU(self, data):
        ''' plot cpu data
            @see: https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt-for-dummies
        '''

        for ax in self.figure.axes:
                self.figure.delaxes(ax)

        color = ['orange', 'blue']
        
        # multicore
        if(len(data) == 4):
            
            ax1 = self.figure.add_subplot(221)
            # discards the old graph
            ax1.clear()
            ax1.pie([100.0-data[0], data[0]], colors=color, autopct=lambda p: '{:.0f}%'.format(p))

            ax2 = self.figure.add_subplot(222)
            # discards the old graph
            ax2.clear()
            ax2.pie([100.0-data[1], data[1]], colors=color, autopct=lambda p: '{:.0f}%'.format(p))

            ax3 = self.figure.add_subplot(223)
            # discards the old graph
            ax3.clear()
            ax3.pie([100.0-data[2], data[2]], colors=color, autopct=lambda p: '{:.0f}%'.format(p))

            ax4 = self.figure.add_subplot(224)
            # discards the old graph
            ax4.clear()
            ax4.pie([100.0-data[3], data[3]], colors=color, autopct=lambda p: '{:.0f}%'.format(p))

        elif (len(data) == 2 ):
            ax1 = self.figure.add_subplot(211)
            # discards the old graph
            ax1.clear()
            ax1.pie([100.0-data[0], data[0]], colors=color, autopct=lambda p: '{:.0f}%'.format(p))

            ax2 = self.figure.add_subplot(212)
            # discards the old graph
            ax2.clear()
            ax2.pie([100.0-data[1], data[1]], colors=color, autopct=lambda p: '{:.0f}%'.format(p))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())