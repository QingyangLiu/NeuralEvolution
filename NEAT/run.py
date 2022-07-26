import Genome
import random
import Crossover
import Species
import math


currGeneration=0
numSamples=10
numInput=2
numOutput=1
nextInnov=numInput

threshold=0.1
disjointConst=0.1
excessConst=0.1

GenerationOffspring=[]
listOfSpecies=[]
mutateWeightRate=0.08
mutateConnRate=0.04
mutateNodeRate=0.02


def main():
	global GenerationOffspring
	global listOfSpecies

	initGenomes()
	for x in range(0, 10000000):
		print("iteration: "+str(x))
		iteration()
		num=0
		for species in listOfSpecies:
			print("Species: "+str(num))
			num+=1
			for genome in species.GenesWithinSpecies:
				print("innov number: "+str(nextInnov))
				genome.printConnection()
				print(Evaluation(genome))
				
					
		#input()
	
		

def iteration():
	global listOfSpecies
	global GenerationOffspring
	listOfSpecies=[]
	Speciation()
	for x in GenerationOffspring:
		x.score=Evaluation(x)
		
	for species in listOfSpecies:
		for genome in species.GenesWithinSpecies:
			genome.score=genome.score/len(species.GenesWithinSpecies)
	GenerationOffspring.clear()
	for species in listOfSpecies:
		SpeciesCrossover(species)
	# for genome in GenerationOffspring:
	# 	containedConnections={}
	# 	for connection in list(genome.connectionList):
	# 		if (connection.inputNode, connection.outputNode) in containedConnections:
	# 			print("removed")
	# 			genome.connectionList.remove(connection)
	# 		else:
	# 			containedConnections[(connection.inputNode, connection.outputNode)]=True


def SpeciesCrossover(species):
	global GenerationOffspring
	global nextInnov

	listOfGenomes=list(species.GenesWithinSpecies)
	listOfGenomes=sorted(listOfGenomes, key=lambda x: x.score, reverse=True)
	
	BestGene=listOfGenomes[0]

	secondBestGene=BestGene
	if (len(listOfGenomes)>1):
		secondBestGene=listOfGenomes[1]
	
	x=0
	while(x<len(species.GenesWithinSpecies)):
		originalInnov=nextInnov
		childGenome=Crossover.crossOver(BestGene, secondBestGene)
		if (random.random()<=mutateWeightRate):
			Crossover.mutateWeights(childGenome.connectionList)
		if (random.random()<=mutateConnRate):
			if (Crossover.mutateAddConnection(childGenome.nodeList, childGenome.connectionList, nextInnov)):
				nextInnov+=1
		if (random.random()<=mutateNodeRate):
			if (Crossover.mutateAddNode(childGenome.nodeList, childGenome.connectionList, nextInnov)):
				nextInnov+=2

		if (Crossover.detectCycle(childGenome.connectionList)==True):
			print("Found")
			x-=1
			nextInnov=originalInnov
			#print("Found")
		else:
			GenerationOffspring.append(childGenome)
		x+=1




def initGenomes():
	global GenerationOffspring
	global listOfSpecies
	for x in range(0, numSamples):
		currGenome=Genome.Genome(numInput, numOutput)
		currGenome.initGenome()
		GenerationOffspring.append(currGenome)

def Speciation():
	global GenerationOffspring
	global listOfSpecies

	for x in GenerationOffspring:
		inserted=False
		for species in listOfSpecies:
			inserted=species.partOfSpecies(x, threshold)
			if inserted==True:
				species.GenesWithinSpecies.append(x)
				break
		if inserted==False:
			newSpecies=Species.Species(disjointConst,excessConst)
			newSpecies.GenesWithinSpecies.append(x)
			listOfSpecies.append(newSpecies)



def Evaluation(genome):
	score=0
	genome.setInput([0,0])
	actualOutput=genome.feedForward()
	if (actualOutput[0]<=0.5):
		score+=1
	genome.setInput([1,0])
	actualOutput=genome.feedForward()
	if (actualOutput[0]>0.5):
		score+=1
	genome.setInput([0,1])
	actualOutput=genome.feedForward()
	if (actualOutput[0]>0.5):
		score+=1
	genome.setInput([1,1])
	actualOutput=genome.feedForward()
	if (actualOutput[0]<=0.5):
		score+=1
	return score



if __name__=="__main__":
	main()





#Crossover.mutateAddConnection(gene.nodeList, gene.connectionList)
#for x in gene.connectionList:
#	print("innov: "+str(x.innov)+" weight: "+str(x.weight)+" inputID: "+str(x.inputNode)+" outputID: "+str(x.outputNode)+" enabled: "+str(x.enabled))
