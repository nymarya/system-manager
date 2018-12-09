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
        command = "kill -9 " + str(pid) 
        try:
            subprocess.call([command], shell=True)
            mb = QtGui.QMessageBox ("","Processo morto com sucesso",QtGui.QMessageBox.Warning,QtGui.QMessageBox.Ok,0,0)
            mb.exec_()
        except:
            mb = QtGui.QMessageBox ("","Não foi possível matar processo",QtGui.QMessageBox.Warning,QtGui.QMessageBox.Ok,0,0)
            mb.exec_()


    def infoProcess(self, pid, com, index):

        command = "ps -p "+ str(pid) +" -o pid,vsz=MEMORY -o user -o comm -o ppid -o stime > info.txt"

        # gera arquivo com informacoes do processo
        subprocess.call([command], shell=True)
        
        # abre arquivo com informacoes
        arc = open('info.txt', 'r')
        # le cada linha do arquivo
        text = arc.readlines()
        # fecha arquivo
        arc.close()

        # separa informacoes        
        infos = text[1].split()

        # mostra informacoes
        message = "INFORMAÇÕES DO PROCESSO: \n PID: "+infos[0]+" \n Memória usada (número decimal de kb): "+infos[1]+"\n Usuário: "+infos[2]+" \n Comando: "+infos[3]+" \n PPID: "+infos[4]+" \n Início da execução às: "+infos[5]
        mb = QtGui.QMessageBox ("",message,QtGui.QMessageBox.Information,QtGui.QMessageBox.Ok,0,0)
        mb.exec_()


    def treeProcess(self, pid, com, index):
        command = "pstree -p "+str(pid)+" > tree.txt"
        subprocess.call([command], shell=True)

        # abre arquivo com informacoes
        arc = open('tree.txt', 'r')
        # le cada linha do arquivo
        text = arc.read()
        # fecha arquivo
        arc.close()
        
        mb = QtGui.QMessageBox ("",text,QtGui.QMessageBox.Information,QtGui.QMessageBox.Ok,0,0)
        mb.exec_()


