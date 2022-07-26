import math 
import random
import numpy as np

class Node:
	def __init__(self, id, type, initVal):
		self.id=id
		self.type=type
		self.val=initVal

	

class Connection:
	def __init__(self, inputNode, outputNode, weight, enabled, innov):
		self.inputNode=inputNode
		self.outputNode=outputNode
		self.weight=weight
		self.enabled=enabled
		self.innov=innov


class Genome:
	def __init__(self, numInputs, numOutputs):
		self.nodeList=[]
		self.connectionList=[]
		self.numInputs=numInputs
		self.numOutputs=numOutputs
		self.score=0

	def initGenome(self):
		self.nodeList=[]
		self.connectionList=[]
		startID=0
		for x in range(self.numOutputs):
			self.nodeList.append(Node(startID, 'output', -float('inf')))
			startID+=1
		for x in range(self.numInputs):
			self.nodeList.append(Node(startID, 'sensor', -float('inf')))
			startID+=1
		startInnov=0
		for x in self.nodeList:
			if x.type=='sensor':
				for y in self.nodeList:
					if y.type=='output':
						self.connectionList.append(Connection(x.id, y.id, np.random.randn(), True, startInnov))
						startInnov+=1



	def printConnection(self, onlyEnabled=False):
		for x in self.connectionList:
			if onlyEnabled==True:
				if x.enabled==True:
					print("innov: "+str(x.innov)+" weight: "+str(x.weight)+" inputID: "+str(x.inputNode)+" outputID: "+str(x.outputNode)+" enabled: "+str(x.enabled))
			else:
				print("innov: "+str(x.innov)+" weight: "+str(x.weight)+" inputID: "+str(x.inputNode)+" outputID: "+str(x.outputNode)+" enabled: "+str(x.enabled))


	def clearGenome(self):
		for x in self.nodeList:
			if x.type=='hidden' or x.type=='output':
				x.val=-float('inf')

	def setInput(self, inputList):
		for x in range(0,len(inputList)):
			self. nodeList[x+self.numOutputs].val=inputList[x]

	def forwardProp(self, nodeID):
		Node=None
		for x in self.nodeList:
			if x.id==nodeID:
				Node=x
				break
		returnVal=0
		if Node!=None and Node.type=='sensor':
			return Node.val
		for connection in self.connectionList:
			if connection.outputNode==nodeID and connection.enabled==True:
				returnVal+=self.forwardProp(connection.inputNode)*connection.weight
		#print(str(nodeID)+": "+str(returnVal))
		
		
		return sigmoid(returnVal)

	def feedForward(self):
		returnOutput=[]
		for x in self.nodeList:
			if x.type=='output':
				returnOutput.append(self.forwardProp(x.id))
		return returnOutput



def sigmoid(x):
  return 1 / (1 + math.exp(-x))






def speciationScore(connectionList1, connectionList2, disjointConst, excessConst):
	longestListSize=len(connectionList1)
	shortestListSize=len(connectionList2)
	numDisjoint=0
	numExcess=0
	if (len(connectionList2)>longestListSize):
		longestListSize=len(connectionList2)
		shortestListSize=len(connectionList1)
	dictList1={}
	dictList2={}
	largestInnovIn1=-float('inf')
	largestInnovIn2=-float('inf')

	for x in connectionList1:
		dictList1[x.innov]=x
		if (x.innov>largestInnovIn1):
			largestInnovIn1=x.innov

	for x in connectionList2:
		dictList2[x.innov]=x
		if (x.innov>largestInnovIn2):
			largestInnovIn2=x.innov
	largestInnov=largestInnovIn1
	smallestInnov=largestInnovIn2
	if (largestInnovIn2>largestInnov):
		largestInnov=largestInnovIn2
		smallestInnov=largestInnovIn1
	for i in range(0, largestInnov+1):
		if (dictList1.__contains__(i)==True and dictList2.__contains__(i)==False) or (dictList1.__contains__(i)==False and dictList2.__contains__(i)==True):
			if (i<=smallestInnov):
				
				numDisjoint+=1
			else:
				numExcess+=1

			
	return numDisjoint*disjointConst/longestListSize+numExcess*excessConst/longestListSize


# gene=Genome(2,1)
# gene.initGenome()
# inputList=[1.0, 2.0]
# gene.setInput(inputList)
# print(forwardProp(gene.nodeList, gene.connectionList, 0))







