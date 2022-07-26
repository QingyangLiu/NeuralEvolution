

class Species:
	def __init__(self, disjointConst, excessConst):
		self.GenesWithinSpecies=[]
		self.disjointConst=disjointConst
		self.excessConst=excessConst



	def partOfSpecies(self, genome, threshold):
		if len(self.GenesWithinSpecies)>0:
			if self.speciationScore(genome.connectionList, self.GenesWithinSpecies[0].connectionList, self.disjointConst, self.excessConst)<=threshold:
				return True
		return False



	def speciationScore(self, connectionList1, connectionList2, disjointConst, excessConst):
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
