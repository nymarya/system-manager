from PyQt4 import QtGui, QtCore
import subprocess


def listProcesses():
    subprocess.call(["ps -eo user,pid,command > processes.txt"], shell=True)

    # abre arquivo com informacoes
    arc = open('processes.txt', 'r')
    # le cada linha do arquivo
    text = arc.readlines()
    # fecha arquivo
    arc.close()
    
    return text
    

def killProcess(pid, com, index):
    print(pid)        



def infoProcess(pid, com, index):
    print(pid)        
