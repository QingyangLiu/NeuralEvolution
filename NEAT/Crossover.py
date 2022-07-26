import random
import Genome
import numpy as np
import networkx as nx

def crossOver(parent1, parent2):
	childNodeList=[]
	childConnectionList=[]

	dictOfConnections1={}
	dictOfConnections2={}
	highestInnovForP1=-float('inf')
	highestInnovForP2=-float('inf')
	for x in parent1.connectionList:
		dictOfConnections1[x.innov]=x
		if x.innov>highestInnovForP1:
			highestInnovForP1=x.innov

	for x in parent2.connectionList:
		dictOfConnections2[x.innov]=x
		if x.innov>highestInnovForP2:
			highestInnovForP2=x.innov

	useHighestScore=highestInnovForP1
	if (parent1.score<parent2.score):
		useHighestScore=highestInnovForP2


	for x in range(0, useHighestScore+1):
		if dictOfConnections1.__contains__(x) and dictOfConnections2.__contains__(x):
			childConnectionList.append(random.choice([dictOfConnections1[x], dictOfConnections2[x]]))
		elif dictOfConnections1.__contains__(x) and ~dictOfConnections2.__contains__(x):
			if (parent1.score > parent2.score):
				childConnectionList.append(dictOfConnections1[x])
		elif ~dictOfConnections1.__contains__(x) and dictOfConnections2.__contains__(x):
			if (parent2.score > parent1.score):
				childConnectionList.append(dictOfConnections2[x])

	
	listOfNodesAdded={}
	for node in parent1.nodeList:
		if node.type=='output' or node.type=='sensor':
			childNodeList.append(node)
			listOfNodesAdded[node.id]=True

	for connect in childConnectionList:
		if listOfNodesAdded.__contains__(connect.inputNode)==False:
			childNodeList.append(Genome.Node(connect.inputNode, 'hidden', -float('inf')))
			listOfNodesAdded[connect.inputNode]=True
	child=Genome.Genome(parent1.numInputs, parent1.numOutputs)
	child.nodeList=childNodeList
	child.connectionList=childConnectionList
	containedConnections={}
	for connection in list(child.connectionList):
		if (connection.inputNode, connection.outputNode) in containedConnections:
			child.connectionList.remove(connection)
		else:
			containedConnections[(connection.inputNode, connection.outputNode)]=True
	return child



def mutateWeightsHelper(inputWeight):
    #0=random weights, 1=multiply weights, 2=add to weight, 3=flip sign
    mutateForm=random.choice([0,1,2,3])
    if mutateForm==0:
        return 2*random.random()-1.0
    elif mutateForm==1:
        return random.uniform(0.0, 2.0)*inputWeight
    elif mutateForm==2:
        return inputWeight+random.random()
    elif mutateForm==3:
        return -1.0*inputWeight

def mutateWeights(connectionList):
	#connectionToMutate.weight=connectionToMutate.weight*random.uniform(-2.0, 2.0)
	connectionToMutate=random.choice(connectionList)
	connectionToMutate.weight=mutateWeightsHelper(connectionToMutate.weight)


# def detectCycle(connectionList, listTraversed, nodeID):
# 	if listTraversed.__contains__(nodeID) and listTraversed[nodeID]==True:
# 		return True
# 	listTraversed[nodeID]=True
# 	containsCycle=False
# 	for x in connectionList:
# 		if x.enabled==True and x.outputNode==nodeID:
# 			containsCycle=containsCycle or detectCycle(connectionList, listTraversed, x.inputNode)
# 	listTraversed[nodeID]=False
# 	return containsCycle

def detectCycle(connectionList):
	edges=[]
	for connection in connectionList:
		if (connection.enabled==True):
			edges.append((connection.inputNode, connection.outputNode))
	graph=nx.DiGraph(edges)
	if len(list(nx.simple_cycles(graph)))==0 :
		return False
	return True



def mutateAddConnection(nodeList, connectionList, nextInnov):
	highestInnovNum=-float('inf')
	for x in connectionList:
		if x.innov>highestInnovNum:
			highestInnovNum=x.innov
	inputNode=random.choice(connectionList)
	outputNode=random.choice(connectionList)
	if inputNode==outputNode:
		return False
	for connection in connectionList:
		if connection.inputNode==inputNode.inputNode and connection.outputNode==outputNode.outputNode:
			connection.enabled=True
			return True

	if inputNode.inputNode==outputNode.outputNode:
		return False

	
	connectionList.append(Genome.Connection(inputNode.inputNode, outputNode.outputNode, np.random.randn(), True, nextInnov))
	return True

def removeDisabledConnections(connectionList):
	connectionList2=list(connectionList)
	for x in connectionList2:
		if x.enabled==False:
			connectionList.remove(x)

def mutateAddNode(nodeList, connectionList, nextInnov):
	highestID=-float('inf')
	highestInnov=-float('inf')
	for x in nodeList:
		if x.id>highestID:
			highestID=x.id
	for x in connectionList:
		if x.innov>highestInnov:
			highestInnov=x.innov
	connectionToSplit=random.choice(connectionList)
	connectionToSplit.enabled=False
	nodeList.append(Genome.Node(highestID+1, 'hidden', -float('inf')))
	connectionList.append(Genome.Connection(connectionToSplit.inputNode, highestID+1, connectionToSplit.weight, True, nextInnov))
	connectionList.append(Genome.Connection(highestID+1, connectionToSplit.outputNode, np.random.randn(), True, nextInnov+1))
	return True


