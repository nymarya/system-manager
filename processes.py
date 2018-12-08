from PyQt4 import QtCore
from time import sleep
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import subprocess

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
        print("stop")
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


