
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import random
import numpy
import networkx as nx
from networkReader import NetworkReader

class Network:

	def __init__(self):
		self.type = ""
		self.model = "LN"
		self.graph = nx.DiGraph()
		self.edges = ""
		self.minTransaction = 1.5

		self.lowDegreeNodeList = []
		self.midDegreeNodeList = []
		self.highDegreeNodeList = []

	# N = number of Nodes
	# T = ['LN', 'ER', 'BA', 'SF,RND] -> Lightning Network, Erdos Rehnyi, Scale-Free/Barabasi
	def create_network(self, N, T, p=0.1):
		self.type = T

		if(T == 'LN'):
			i = 0
			#Currently being done in LoadModule.py not here, will eventually move it
		elif(T == 'ER'): # random_geometric_graph
			graph1 = nx.erdos_renyi_graph(N,p, seed=1)
			self.graph.add_edges_from(graph1.edges())
		elif(T == 'BA'):
			m = 1 # Number of edges to attach from a new node to existing nodes
			graph1 = nx.barabasi_albert_graph(N,m, seed=1)
			self.graph.add_edges_from(graph1.edges())
		elif(T == 'SF'):
			graph1 = nx.scale_free_graph(N)
			self.graph.add_edges_from(graph1.edges())
		elif(T == 'RND'):
			graph1 = nx.fast_gnp_random_graph(N, p)
			self.graph.add_edges_from(graph1.edges())

	def show_graph(self):
		nx.draw(self.graph)
		plt.show()

	def create_link_capacities(self, edgeList):
		self.filter_degree()
		self.add_capacities()
		
		print(len(self.graph.edges()))
		self.add_missing_edges()
		print(len(self.graph.edges()))
		self.add_missing_capacities()
		print(len(self.graph.edges()))
		self.make_edge_list(edgeList)

	def filter_degree(self):
		nodeDegree = self.graph.degree()

		for node in nodeDegree():
			if(node[1] < 4):
				self.lowDegreeNodeList.append(node)
			elif(node[1] <= 10):
				self.midDegreeNodeList.append(node)
			elif(node[1] > 10):
				self.highDegreeNodeList.append(node)

	def add_capacities(self):
		for edge in self.graph.edges():
			for e in self.lowDegreeNodeList:
				if(e[0] == edge[0]):
					self.graph[edge[0]][edge[1]]['capacity'] = self.get_capacity_value(0)
					break

			for e in self.midDegreeNodeList:
				if(e[0] == edge[0]):
					self.graph[edge[0]][edge[1]]['capacity'] = self.get_capacity_value(1)
					break

			for e in self.highDegreeNodeList:
				if(e[0] == edge[0]):
					self.graph[edge[0]][edge[1]]['capacity'] = self.get_capacity_value(2)
					break

	def get_capacity_value(self, degreeClassification):
		v = 0

		if(degreeClassification == 0):
			if(self.model == 'XRP'):
				v = self.minTransaction * random.random() * 200
			elif(self.model == 'LN'):
				beta = 1.0/250
				v = numpy.random.exponential(beta)
		elif(degreeClassification == 1):
			if(self.model == 'XRP'):
				v = self.minTransaction * random.random() * 800
			elif(self.model == 'LN'):
				beta = 1.0/800
				v = numpy.random.exponential(beta)
		elif(degreeClassification == 2):
			if(self.model == 'XRP'):
				v = self.minTransaction * random.random() * 5000
			elif(self.model == 'LN'):
				beta = 1.0/5000
				v = numpy.random.exponential(beta)
		return v

	def add_missing_edges(self):
		missingNodes = []

		triggered = True
		for n in self.graph.nodes():
			for e in self.graph.edges():
				if(n == e[1]):
					triggered = False
			if(not triggered):
				missingNodes.append(n)

		for edge in self.graph.edges(data=True):
			for node in missingNodes:
				if(edge[1] == node):
					self.add_bi_direction(node, edge[0], edge[2]['capacity'])

	def add_missing_capacities(self):
		# Reverse list
		edges = self.graph.edges()

		for nodeLow in self.lowDegreeNodeList:
			l = len(edges(nodeLow[0]))
			for i in range(0, l):
				degree = len(edges(nodeLow[0]))
				if(degree == 1):
					self.add_bi_direction(nodeLow[1], nodeLow[0], 0)
				else:
					self.add_bi_direction(nodeLow[1], nodeLow[0], 0) 	

		for nodeMid in self.midDegreeNodeList:
			l = len(edges(nodeMid[0]))
			for i in range(0, l):
				degree = len(edges(nodeMid[0]))
				if(degree  <  7):
					self.add_bi_direction(nodeMid[1], nodeMid[0], random.random() * 100)
				else:
					self.add_bi_direction(nodeMid[1], nodeMid[0], random.random() * 100) 

		for nodeHigh in self.highDegreeNodeList:
			l = len(edges(nodeHigh[0]))
			for i in range(0, l):
				degree = len(edges(nodeHigh[0]))
				if(degree < 12):		
					self.add_bi_direction(nodeHigh[1], nodeHigh[0], random.random() * 10000)
				else:
					self.add_bi_direction(nodeHigh[1], nodeHigh[0], random.random() * 10000) 

	def make_edge_list(self, edgeList):
		curNode = 0
		lenNodes = len(self.graph.edges())
		for curNode in range(0,lenNodes):
			for e1 in self.graph.edges(data=True):
				if(curNode == e1[0]):
					edgeList.append(e1)

		lenList = len(edgeList)
		for i in range(lenList-1, -1, -1):
			if(edgeList[i][0] == edgeList[i][1]):
				del edgeList[i]

	def add_bi_direction(self, sender, receiver, cap): 
		self.graph.add_edge(sender, receiver, capacity=cap)

	def create_transaction_list(self, numTransactions, transList):

		numNodes = len(self.graph.nodes())
		time = 0
		tList = []

		if(self.model == "LN"):
			lowDegreeTransaction = int(numTransactions / 2)
			midDegreeTransaction = int(numTransactions / 3)
			highDegreeTransaction = int(numTransactions / 9)
		elif(self.model == "XRP"):
			lowDegreeTransaction = int(numTransactions / 3)
			midDegreeTransaction = int(numTransactions / 3)
			highDegreeTransaction = int(numTransactions / 3)

		for x in range(0, lowDegreeTransaction):
			node = int(random.randint(0, len(self.lowDegreeNodeList)-1))
			hop_count = random.randint(1,4)
			paths = (nx.single_source_shortest_path(self.graph, 3))
			path_with_hop_count = []
			for key in paths.keys():
				if(hop_count == len(paths[key])):
					path_with_hop_count.append(int(key))
			destIndex = random.randint(0, len(path_with_hop_count)-1)
			dest = path_with_hop_count[destIndex]
			tList.append((node, dest, self.create_transaction_amount(0)))

		for x in range(0, midDegreeTransaction):
			node = int(random.randint(0, len(self.midDegreeNodeList)-1))
			hop_count = random.randint(1,4)
			paths = (nx.single_source_shortest_path(self.graph, 3))
			path_with_hop_count = []
			for key in paths.keys():
				if(hop_count == len(paths[key])):
					path_with_hop_count.append(int(key))
			destIndex = random.randint(0, len(path_with_hop_count)-1)
			dest = path_with_hop_count[destIndex]
			tList.append((node, dest, self.create_transaction_amount(1)))

		for x in range(0, highDegreeTransaction):
			node = int(random.randint(0, len(self.highDegreeNodeList)-1))
			hop_count = random.randint(1,4)
			paths = (nx.single_source_shortest_path(self.graph, 3))
			path_with_hop_count = []
			for key in paths.keys():
				if(hop_count == len(paths[key])):
					path_with_hop_count.append(int(key))
			destIndex = random.randint(0, len(path_with_hop_count)-1)
			dest = path_with_hop_count[destIndex]
			tList.append((node, dest, self.create_transaction_amount(2)))

		time = 0;
		elements = len(tList)
		for x in range(0,elements):
			tranI = random.randint(0,len(tList)-1)
			transList.append((time,tList[tranI][0], tList[tranI][1], tList[tranI][2]))
			time = time + random.uniform(0,5)

	def create_transaction_amount(self, transactionClassification):

		if(self.model == "LN"):
			if(transactionClassification == 0):
				return random.uniform(1, 20)

			elif(transactionClassification == 1):
				return random.uniform(10, 400)

			elif(transactionClassification == 2):
				return random.uniform(30, 1000)

		elif(self.model == "XRP"):
			if(transactionClassification == 0):
				return random.uniform(1, 20)

			elif(transactionClassification == 1):
				return random.uniform(10, 400)

			elif(transactionClassification == 2):
				return random.uniform(30, 1000)

	def add_edges(self, edgeList):
		self.graph.add_edges_from(edgeList)