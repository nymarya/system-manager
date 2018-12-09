from PyQt4 import QtCore
from time import sleep
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import subprocess

class ProcessStatusListener(QtCore.QThread):

    def __init__(self, parent = None):
    
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.states = { "D": ["uninterruptible sleep",'magenta'],
                        'R': ["running or runnable",'yellow'],
                        'I': ["Idle kernel thread",'cyan'],
                        'S': ["interruptible sleep",'green'],
                        'T': ["stopped by job control signal",'blue'],
                        't': ["stopped by debugger",'lightgreen'],
                        'W': ["paging",'lightblue'],
                        'X': ["dead", 'red'],
                        'Z': ["defunct", 'gray'],
                        }

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
            subprocess.call(["ps -eo state=|sort|uniq -c > processes.txt"], shell=True)
            # abre arquivo com informacoes
            arc = open('processes.txt', 'r')
            # le cada linha do arquivo
            text = arc.readlines()
            # fecha arquivo
            arc.close()

            # Formata dados
            labels = []
            values = []
            colors = []
            for data in text:
                value,label = data.split()
                values.append(int(value))
                labels.append(self.states[label][0])
                colors.append(self.states[label][1])

            result = [labels, values, colors]
            self.emit(SIGNAL("output(PyQt_PyObject)"),result)
            
            sleep(1)




