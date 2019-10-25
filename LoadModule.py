from network import Network
from node import Node
import os
from networkReader import NetworkReader
from create_network import CreateNedFile

class LoadModule:

	def __init__(self):
		self.network = Network()
		self.nodeAmount = 250
		self.type = "BA"
		self.edgeList = []
		self.transactionList = []
		self.nodeList = []

	def save_edge_list(self):
		fileName = './results/'+ str(self.nodeAmount) + "_" + self.type + "_link_capacities"
		fileCount = 1

		fileExists = True
		while(fileExists):
			fileExists = os.path.isfile(fileName + '_' + str(fileCount) + '.txt')
			if(fileExists):
				fileCount = fileCount + 1

		fileName = fileName + '_' + str(fileCount) + '.txt'
		file = open(fileName, 'a+')

		file.write('sender,receiver,capacity\n')

		for edge in self.edgeList:
			file.write(str(edge[0]) + "," + str(edge[1]) + "," + str(edge[2]['capacity'])  + "\n")

	def save_trans_list(self):
		fileName = './results/'+ str(self.nodeAmount) + "_" + self.type + "_transactions"
		fileCount = 1

		fileExists = True
		while(fileExists):
			fileExists = os.path.isfile(fileName + '_' + str(fileCount) + '.txt')
			if(fileExists):
				fileCount = fileCount + 1

		fileName = fileName + '_' + str(fileCount) + '.txt'
		file = open(fileName, 'a+')

		file.write('time,sender,destination,amount\n')

		for trans in self.transactionList:
			file.write(str(trans[0]) + "," + str(trans[1]) + "," + str(trans[2]) + "," + str(trans[3])  + "\n")


	def load_lightning_network(self):
		networkReader = NetworkReader('networkgraphv2.txt')
		networkReader.load_file(True)
		self.nodeAmount = networkReader.numNodes
		self.network.add_edges(networkReader.edgeList)
		self.edgeList = networkReader.edgeList

		self.network.filter_degree()
		self.network.create_transaction_list(100, self.transactionList)

		self.save_edge_list()
		self.save_trans_list()

		return networkReader.edgeList

	def create_NED(self):
		nedFile = CreateNedFile()
		nedFile.nodeList = self.network.graph.nodes()
		nedFile.edgeList = self.network.graph.edges()
		nedFile.amountOfNodes = len(self.network.graph.nodes())

		nedFile.save_file()


if __name__ == '__main__':
	loadmodule = LoadModule()
	
	## reads the lightning json files and creates an edge list
	# loadmodule.load_lightning_network()

	#loadmodule.save_edge_list()

	## creates an own network and creates an edge list
	loadmodule.network.create_network(loadmodule.nodeAmount, loadmodule.type, p=0.2)
	loadmodule.network.show_graph()
	loadmodule.network.create_link_capacities(loadmodule.edgeList)
	loadmodule.save_edge_list()
	loadmodule.network.create_transaction_list(100, loadmodule.transactionList)
	loadmodule.save_trans_list()
	loadmodule.create_NED()