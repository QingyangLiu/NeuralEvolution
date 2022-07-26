import numpy as np 
import random



class Genotype:
    def __init__(self, syn0, syn1):
        self.syn0=syn0
        self.syn1=syn1
        self.score=-float('inf')


    def nonlin(self, x):
        return 1/(1+np.exp(-x))

    def getOutput(self, x):
         #forward pass algorithm based on algorithm by Siraj Raval https://www.youtube.com/watch?v=h3l4qz76JhQ
        l0=x
        l1=self.nonlin(np.dot(l0, self.syn0))
        l2=self.nonlin(np.dot(l1,self.syn1))
        return l2


def nonlin(x, deriv=False):
    if deriv==True:
        return x*(1-x)

    return 1/(1+np.exp(-x))




def mutateWeights(inputWeight):
    #0=random weights, 1=multiply weights, 2=add to weight, 3=flip sign
    mutateForm=random.choice([0,1,2,3])
    if mutateForm==0:
        return 2*random.random()-1
    elif mutateForm==1:
        return random.uniform(0.0, 2.0)*inputWeight
    elif mutateForm==2:
        return inputWeight+random.random()
    elif mutateForm==3:
        return -1.0*inputWeight


def crossOver(genome1, genome2, mutationChance):
    childsyn0=genome1.syn0.copy()
    childsyn1=genome1.syn1.copy()
    mutated=False
    for i in range(len(childsyn0)):
        for j in range(len(childsyn0[0])):
            childsyn0[i][j]=random.choice([genome1.syn0[i][j], genome2.syn0[i][j]])
            if random.random()<=mutationChance and mutated==False:
               
               childsyn0[i][j]=mutateWeights(childsyn0[i][j])
               mutated=True

    for i in range(len(childsyn1)):
        for j in range(len(childsyn1[0])):
            childsyn1[i][j]=random.choice([genome1.syn1[i][j], genome2.syn1[i][j]])
            if random.random()<=mutationChance and mutated==False:
                childsyn1[i][j]=mutateWeights(childsyn1[i][j])
                mutated=True

    return Genotype(childsyn0, childsyn1)



def getScore(actualVal, expectedVal):
    score=0
    for i in range(0, len(actualVal)):
        if expectedVal[i][0]==1 and actualVal[i]>0.9:
            score+=1
        elif expectedVal[i][0]==0 and actualVal[i]<=0.1:
            score+=1
    return score

def diffGetScore(actualVal, expectedVal):
    score=0
    for i in range(0, len(actualVal)):
        score+=float(abs((actualVal[i]-expectedVal[i][0])))

    return score*-1.0

input=np.array([[1,0,0],
            [1,0,1],
            [1,1,0],
            [1,1,1]])
output=np.array([[0],
            [1],
            [1],
            [0]])

numPop=10

syn0=2*np.random.random((3,4))-1
syn1=2*np.random.random((4,1))-1


genomeList=[]
for i in range(0, numPop):
    genomeList.append(Genotype(2*np.random.random((3,8))-1, 2*np.random.random((8,1))-1))

for j in range(600000):

    for genome in genomeList:
        genome.score=diffGetScore(genome.getOutput(input),output)
    genomeList.sort(key=lambda x: x.score, reverse=True)
    if j%1000==0:
        print("Generation: "+str(j))
        for x in genomeList:


            print(x.score)
            print(genome.getOutput(input))

    highestGenome=genomeList[0]
    secondHighest=genomeList[1]
    genomeList.clear()
    for i in range(0, numPop):
        genomeList.append(crossOver(highestGenome, secondHighest,0.08))
        #genomeList.append(Genotype(2*np.random.random((3,8))-1, 2*np.random.random((8,1))-1))








    




