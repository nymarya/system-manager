from PyQt4 import QtGui, QtCore
import subprocess


class ManagerProcesses:

    def listProcesses(self):
        subprocess.call(["ps -eo user,pid,command > processes.txt"], shell=True)

        # abre arquivo com informacoes
        arc = open('processes.txt', 'r')
        # le cada linha do arquivo
        text = arc.readlines()
        # fecha arquivo
        arc.close()
        
        return text
        

    def killProcess(self, pid, com, index):
        subprocess.call(["kill -9 23467"], shell=True)
        mb = QtGui.QMessageBox ("","Processo excluído com sucesso",QtGui.QMessageBox.Warning,QtGui.QMessageBox.Ok,0,0)
        mb.exec_()


    def infoProcess(self, pid, com, index):
        subprocess.call()
        mb = QtGui.QMessageBox ("","INFORMACOES DO PROCESSO",QtGui.QMessageBox.Information,QtGui.QMessageBox.Ok,0,0)
        mb.exec_()