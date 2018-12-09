from PyQt4 import QtCore
from time import sleep
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import subprocess

class ProcessStatusListener(QtCore.QThread):

    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.isCPU = False
        # @see http://man7.org/linux/man-pages/man1/ps.1.html#PROCESS_STATE_CODES
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
        #self.__del__()


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

class CPUListener(QtCore.QThread):

    def __init__(self, parent = None):
    
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.isCPU = True

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
            cpu_number = subprocess.check_output(["grep 'cpu' /proc/stat | wc -l"], shell=True)

            result = []
            # Formata dados
            # @see https://stackoverflow.com/questions/3017162/how-to-get-total-cpu-usage-in-linux-using-c/3017438#3017438
            for i in range(0, int(cpu_number)-1):
                cpu = 'cpu'+str(i)
                all_use = "$2+$3+$4+$9"
                work = "$5"
                total_query = "grep '"+cpu+"' /proc/stat | awk '{usage=("+all_use+")} END {print usage}'"
                work_query = "grep '"+cpu+"' /proc/stat | awk '{usage=("+work+")} END {print usage}'"

                prev_non_idle = subprocess.check_output([total_query],shell=True)
                prev_idle = subprocess.check_output([work_query],shell=True)

                sleep(0.05)

                non_idle = subprocess.check_output([total_query],shell=True)
                idle = subprocess.check_output([work_query],shell=True)

                prev_total = int(prev_idle) + int(prev_non_idle)
                total = int(idle) + int(non_idle)

                #So the %cpu usage over this period is:
                totald = int(total)- int(prev_total)

                idled = int(idle) - int(prev_idle)

                try:
                    cpu_usage = (totald - idled)/totald * 100
                except:
                    cpu_usage=0    
                result.append(cpu_usage)

            self.emit(SIGNAL("output(PyQt_PyObject)"),result)
            
            sleep(1)




