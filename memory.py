import subprocess


# abre arquivo de informacoes sobre memoria
arc = open('/proc/meminfo', 'r')
# le cada linha do arquivo
text = arc.readlines()

# recupera cada palavra da linha
memTotalSplit = text[0].split(" ")
memFreeSplit = text[1].split(" ")
memAvailableSplit = text[2].split(" ")
memCachedSplit = text[4].split(" ")
swapTotalSplit = text[14].split(" ")
swapFreeSplit = text[15].split(" ")

# recupera apenas o valor e transforma pra int
memTotal = int(memTotalSplit[-2])
memFree = int(memFreeSplit[-2])
memAvailable = int(memAvailableSplit[-2])
memCached = int(memCachedSplit[-2])
swapTotal = int(swapTotalSplit[-2])
swapFree = int(swapFreeSplit[-2])

# fecha arquivo
arc.close()


# funcao para plotar grafico de pizza
def plot_pizza( labels, values ):
    labels = [labels[0], labels[1]]
    titles = [values[0], values[1]]
    color = ['lightblue', 'green']
    explode = (0.1, 0)  # somente explode primeiro pedaço
    total = sum(titles)
    plt.pie(titles, explode=explode, labels=labels, colors=color, autopct=lambda p: '{:.0f}'.format(p * total / 100), shadow=True, startangle=90)



# PLOTAR GRAFICO 1: MEMORIA LIVRE X MEMORIA TOTAL 
def plotGraph1():
	labels1 = ['Mem. Livre', 'Mem. Total']
	values1 = [memFree, memTotal-memFree]

	return [labels1, values1]




# PLOTAR GRAFICO 2: MEMORIA ACESSIVEL X MEMORIA TOTAL 
def plotGraph2():
	labels2 = ['Mem. Acessivel', 'Mem. Total']
	values2 = [memAvailable, memTotal-memAvailable]

	# Determina que as proporções sejam iguais ('equal') de modo a desenhar o círculo
	return [labels2, values2]


# PLOTAR GRAFICO 3: MEMORIA CACHE X MEMORIA TOTAL
def plotGraph3():
	labels3 = ['Mem. Cache', 'Mem. Total']
	values3 = [memCached, memTotal-memCached]

	# Determina que as proporções sejam iguais ('equal') de modo a desenhar o círculo
	return [labels3, values3]


# PLOTAR GRAFICO 4: SWAP TOTAL X MEMORIA TOTAL
def plotGraph4():
	labels4 = ['Swap', 'Mem. Total']
	values4 = [swapTotal, memTotal-swapTotal]

	# Determina que as proporções sejam iguais ('equal') de modo a desenhar o círculo
	return [labels4, values4]


# PLOTAR GRAFICO 5: SWAP TOTAL X SWAP LIVRE
def plotGraph5():
	labels5 = ['Swap Livre', 'Swap Usado']
	values5 = [swapFree, swapTotal - swapFree]

	# Determina que as proporções sejam iguais ('equal') de modo a desenhar o círculo
	return [labels5, values5]


def pageFaults():
	# cria arquivo com informacoes dos processos ativos
    subprocess.call(["ps -eo pid,command,min_flt,maj_flt > pageFaults.txt"], shell=True)


    # abre arquivo com informacoes
    arc = open('pageFaults.txt', 'r')
    # le cada linha do arquivo
    text = arc.readlines()
    # fecha arquivo
    arc.close()

    return text


