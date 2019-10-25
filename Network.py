
import plotly.graph_objects as go
import matplotlib.pyplot as plt

import networkx as nx

class Network:

	def __init__(self):
		self.type = ""
		self.graph = nx.Graph()
		self.edges = ""
		self.minTransaction = 1.5

	# N = number of Nodes
	# T = ['LN', 'ER', 'BA', 'SF,RND] -> Lightning Network, Erdos Rehnyi, Scale-Free/Barabasi
	def create_network(self, N, T, p=0.1):
		self.type = T

		if(T == 'LN'):
			i = 0
			#Must load the lightning topology
		elif(T == 'ER'): # random_geometric_graph
			self.graph = nx.erdos_renyi_graph(N,p)
		elif(T == 'BA'):
			m = 1 # Number of edges to attach from a new node to existing nodes
			self.graph = nx.barabasi_albert_graph(N,m)
		elif(T == 'SF'):
			self.graph = nx.scale_free_graph(N)
		elif(T == 'RND'):
			self.graph = nx.fast_gnp_random_graph(N, p)

	def show_graph(self):
		nx.draw(self.graph)
		plt.show()

	def create_link_capacities(self, edgeList):
		if(self.type == 'BA' or self.type == 'SF'):
			self.create_barabasi_link_capacities(edgeList)

	def create_barabasi_link_capacities(self, edgeList):
		
		nodes = self.graph.degree()
		edges = self.graph.edges()

		lowDegreeNodeList = []
		midDegreeNodeList = []
		highDegreeNodeList = []

		for node in self.graph.degree():
			if(node[1] < 4):
				lowDegreeNodeList.append(node)
			elif(node[1] <= 10):
				midDegreeNodeList.append(node)
			elif(node[1] > 10):
				highDegreeNodeList.append(node)


		for edge in edges:
			for e in lowDegreeNodeList:
				if(e[0] == edge[0]):
					self.graph[edge[0]][edge[1]]['weight'] = self.minTransaction * 10
					break

			for e in midDegreeNodeList:
				if(e[0] == edge[0]):
					print("mid: " + str(e) + " , " + str(edge))
					self.graph[edge[0]][edge[1]]['weight'] = self.minTransaction * 20
					break

			for e in highDegreeNodeList:
				if(e[0] == edge[0]):
					print("hig: " + str(e) + " , " + str(edge))
					self.graph[edge[0]][edge[1]]['weight'] = self.minTransaction * 50
					break

		# Reverse list
		print("hh:" + str(self.graph.nodes[0]))
		for edge in edges:
			for e in lowDegreeNodeList:
				if(e[1] )
				# add an edge to the node graph then print the edge list to see everthing11







