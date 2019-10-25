import json
from node import Edge, Node
import numpy
import matplotlib.pyplot as plt
import seaborn as sns
# nodes: 'alias', 'color', 'pub_key', 'addresses', 'last_update'
# edges: 

class NetworkReader:

	def __init__(self, fName):
		self.fileName = fName

		self.BIDIRECTIONAL = True
		self.biDirectionalPubKey = []
		self.jsonData = None
		self.numNodes = 0
		self.edgeList = []
		self.capacityList = []

	def load_file(self, capacityDistritionFigure):
		# Load file
		with open('networkgraphv2.txt', 'r') as json_file:
			self.jsonData = json.load(json_file)

		self.make_bi_directional_connection_list_pub_keys()

		if(capacityDistritionFigure == True):
			self.capacity_distribution()

	def make_bi_directional_connection_list_pub_keys(self):
		# Make a list of nodes with the alias and pub_key and giving a nodeId
		for i, nodes in enumerate(self.jsonData['nodes'], 0):
			self.biDirectionalPubKey.append(Node(nodes['alias'], nodes['pub_key'], i))

		# Adding the edges to each node
		for i, edge in enumerate(self.jsonData['edges']):
			for node in self.biDirectionalPubKey:
				if(node.pubKey == edge['node1_pub']):
					receiverId = self.find_node_id(edge['node2_pub'])
					node.addEdge(receiverId, edge['node2_pub'], edge['capacity'])
					self.capacityList.append(float(edge['capacity']))
				
				if(node.pubKey == edge['node2_pub'] and self.BIDIRECTIONAL):
					receiverId = self.find_node_id(edge['node1_pub'])
					node.addEdge(receiverId, edge['node1_pub'], edge['capacity'])


		self.numNodes = len(self.biDirectionalPubKey)
		self.make_edge_list()

	def make_edge_list(self):
		edList = []
		for node in self.biDirectionalPubKey:
			print(str(node))
			eList = node.get_edge_list()
			if eList is None:
				continue
			else:
				for edge in eList:
					self.edgeList.append(edge)

	def find_node_id(self, pubKey):
		for node in self.biDirectionalPubKey:
			if(node.pubKey == pubKey):
				return node.numberId

	def capacity_distribution(self):
		capacityListEuro = []

		for cap in self.capacityList:
			cap1 = cap *(7.5/100000)
			if cap1 < 4000:
				capacityListEuro.append(cap *(7.5/100000))
		plt.hist(capacityListEuro,
		                  bins=100,
		                  color='skyblue',
		                  density=True,
		                  linewidth= 15,
		                  alpha=1)
		plt.title('Capacity Distribution Lightning Network October 2019')
		plt.ylabel('Frequency')
		plt.xlabel('Capacity Distribution [euro]')
		plt.savefig('./results/capacity_distribution_lightning.png', dpi=300)
