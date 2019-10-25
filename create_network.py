import random


class CreateNedFile:

	def __init__(self):
		self.startValue = 0
		self.amountOfNodes = 500
		self.amountOfConnections = 2500
		self.numOfConnections = 0

		self.nodeS = "node"
		self.whiteSpaceSmall = "    "
		self.whiteSpaceBig = "        "
		self.fileWriteData = []
		self.listNodes = []
		self.hubNodes = []

		self.nodeList = []
		self.edgeList = []

		self.outS = ".out++"
		self.inS = ".in++"

		self.channelOut = " --> Channel --> "
		self.channelIn = " <-- Channel <-- "

	def create_start_file(self):

		self.fileWriteData.append("package speedymurmurs;")
		self.fileWriteData.append("")
		self.fileWriteData.append("network Network" + str(self.amountOfNodes) + " {")
		self.fileWriteData.append(self.whiteSpaceSmall + "types:")
		self.fileWriteData.append(self.whiteSpaceBig + "channel Channel extends ned.DelayChannel")
		self.fileWriteData.append(self.whiteSpaceBig + "{")
		self.fileWriteData.append(self.whiteSpaceBig + self.whiteSpaceSmall + "delay = 10ms;")
		self.fileWriteData.append(self.whiteSpaceBig + "}")
		self.fileWriteData.append("")


	def create_submodule_section(self):
		self.fileWriteData.append("submodules:")
		for x in range(0, len(self.nodeList)):
			node = ""
			if(x < 10):
				node = self.nodeS + "0000" + str(x)		
			elif(x < 100):
				node = self.nodeS + "000" + str(x)
			elif(x < 1000):
				node = self.nodeS + "00" + str(x)
			elif(x < 10000):
				node = self.nodeS + "0" + str(x)				
			self.fileWriteData.append(self.whiteSpaceBig + node + " : " + "BasicNode;")

		self.fileWriteData.append("")


	def create_channel_connection(self):
		self.fileWriteData.append("connections:")

		pairsAlreadyAdded = []

		for edge in self.edgeList:
			if(edge[0] < 10):
				node1 = self.nodeS + "0000" + str(edge[0])		
			elif(edge[0] < 100):
				node1 = self.nodeS + "000" + str(edge[0])
			elif(edge[0] < 1000):
				node1 = self.nodeS + "00" + str(edge[0])
			elif(edge[0] < 10000):
				node1 = self.nodeS + "0" + str(edge[0])	

			if(edge[1] < 10):
				node2 = self.nodeS + "0000" + str(edge[1])		
			elif(edge[1] < 100):
				node2 = self.nodeS + "000" + str(edge[1])
			elif(edge[1] < 1000):
				node2 = self.nodeS + "00" + str(edge[1])
			elif(edge[1] < 10000):
				node2 = self.nodeS + "0" + str(edge[1])
			if(pairsAlreadyAdded is None):
				pairsAlreadyAdded.append((node2, node1))
				self.add_connection(node1,node2)
			else:
				added = False
				for nodes in pairsAlreadyAdded:
					if(nodes[0] == node1 and nodes[1] == node2):
						added = True
				if(not added):
					pairsAlreadyAdded.append((node2, node1))
					self.add_connection(node1,node2)


			

		self.fileWriteData.append("}")

	def add_connection(self, node1, node2):
		out = str(node1) + self.outS + self.channelOut + str(node2) + self.inS + ";"
		in_ = str(node1) + self.inS + self.channelIn + str(node2) + self.outS + ";"
		self.fileWriteData.append(out)
		self.fileWriteData.append(in_)


	def save_file(self):
		self.create_start_file()
		self.create_submodule_section()
		self.create_channel_connection()
		self.save()

	def save(self):


		f = open("./results/network" + str(self.amountOfNodes) + ".ned", "a+")

		for x in self.fileWriteData:
			f.write(x+"\n")

		f.close()
