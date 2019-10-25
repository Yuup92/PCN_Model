
class Edge:

	def __init__(self, sId, rId, connectedNodePubKey, capacityFromNode):
		self.senderId = sId
		self.receiverId = rId
		self.cNodeAlias = ""
		self.cNodePukKey = connectedNodePubKey
		self.capacityTowardsConnNode = int(capacityFromNode)

		self.updatedCapacityTowardsNode = False
		self.capacityTowardsNode = 0

	def checkPubKey(self, pubKey, alias):
		if(self.cNodePukKey == pubKey):
			self.cNodeAlias = alias 
			return True
		else:
			return False

	def return_edge_networkx(self):
		edge = (self.senderId, self.receiverId)
		weight = {'capacity': self.capacityTowardsConnNode}
		edge = edge + (weight,)
		return edge



class Node:

	def __len__(self):
		return len(self.listEdges)

	def __str__(self):
		value = 0
		res = ""
		res = res + "NodeAlias: " + self.nodeAlias
		res = res + "\n  pubKey:" + self.pubKey 
		res = res + "\n num:" + str(self.numberId)
		res = res + "\n degree: " + str(len(self.listEdges))
		for edge in self.listEdges:
			# res = res + "\n  " + edge.cNodeAlias.decode("ascii")
			value = value + edge.capacityTowardsConnNode

		res = res + "\nvalueCap: " + str(value)
		return res

	def __init__(self, nodeAlias, pubKey, nId):
		self.nodeAlias = nodeAlias
		self.pubKey = pubKey
		self.numberId = nId
		self.listEdges = []

	def get_edge_list(self):
		edgeList = []
		if self.listEdges is None:
			return edgeList
		for edge in self.listEdges:
			edgeList.append(edge.return_edge_networkx())
		return edgeList


	def getPublicKet(self):
		return self.pubKey

	def addEdge(self, receiverId, cNPK, cap):
		edge = Edge(self.numberId, receiverId, cNPK, cap)
		self.listEdges.append(edge)

	def addCapacityFromNode(self, cNPK, cFN):
		for edge in self.listEdges:
			if(edge.cNodePukKey == cNPK):
				edge.capacityTowardsNode = cFN
				edge.updatedCapacityTowardsNode = True

	def addAlias(self, nodeList):
		for node in nodeList:
			for edge in self.listEdges:
				edge.checkPubKey(node['pub_key'], node['alias'])


