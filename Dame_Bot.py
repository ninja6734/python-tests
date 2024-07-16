from random import *
import csv
from math import *

class DameBot:
    type = ""
    InputLayer = []
    HiddenLayers = []
    Weights = []
    Biases = []
    randMinVal = 0
    randMaxVal = 0
    _input = 0

    #initialisation
    def __init__(self, type, HiddenLayerSize, Nodes, firstInit = False) -> None:
        #throw error if input is wrong
        if(len(Nodes) != HiddenLayerSize):
            raise IndexError("Nodes must be the same length as the HiddenLayerSize minus the Ouput Layer (1)")
        self.type = type
        
        #Initialize HiddenLayer
        for i in range(HiddenLayerSize):
            self.HiddenLayers.append([0] * Nodes[i])
        self.HiddenLayers.append([0] * 4096)

        #initialize InputLayer
        self.InputLayer = [0] * 64

        self.createWeightsBiases(HiddenLayerSize, Nodes)

        #init weight randomness
        if(firstInit):
            self.RandomizeInit()
        else:
            self.randomizeValue()

    
    #output
    def __str__(self):
        return f"type: {self.type} HiddenLayers: {self.HiddenLayers[:-1]}"
    
    def createWeightsBiases(self, HiddenLayerSize, Nodes):
        for HiddenLayerNum in range(HiddenLayerSize + 1):
            TempBiases = []
            TempWeights = []
            if(HiddenLayerNum != HiddenLayerSize):
                for _ in range(Nodes[HiddenLayerNum]):
                    TempBiases.append(0)
                    if(HiddenLayerNum == 0):
                        TempWeights.append([0] * len(self.InputLayer))
                    else:
                        TempWeights.append([0] * Nodes[HiddenLayerNum - 1])
            else:
                for _ in range(4096):
                    TempBiases.append(0)
                    TempWeights.append([0] * Nodes[-1])
            self.Weights.append(TempWeights)
            self.Biases.append(TempBiases)

    def randomizeValue(self):
        return random() * (self.randMaxVal - self.randMinVal) + self.randMinVal
    
    def randomizeChangeValue(self):
        return self._input + self.randomizeValue()
    
    def RandomizeInit(self):
        self.SetRandVal(-1,1)
        for x,_ in enumerate(self.Weights):
            for y,_ in enumerate(self.Weights[x]):
                for z,_ in enumerate(self.Weights[x][y]):
                    self.Weights[x][y][z] = self.randomizeValue()
                    
        self.SetRandVal(-12,12)
        for x,_ in enumerate(self.Biases):
            for y,_ in enumerate(self.Biases[x]):
                self.Biases[x][y] = self.randomizeValue()

    def SetRandVal(self,minVal,maxVal ):
        self.randMinVal = minVal
        self.randMaxVal = maxVal
    
    def RandomizeChange(self,cost=1):
        if(cost <= 0):
            costChange = 0.2
        costChange = sqrt(cost) + 0.2
        self.SetRandVal(-costChange,costChange)
        for x,_ in enumerate(self.Weights):
            for y,_ in enumerate(self.Weights[x]):
                for z,_ in enumerate(self.Weights[x][y]):
                    self.Weights[x][y][z] = self.randomizeValue()
                    
        self.SetRandVal(-4 * costChange,4*  costChange)
        for x,_ in enumerate(self.Biases):
            for y,_ in enumerate(self.Biases[x]):
                self.Biases[x][y] = self.randomizeValue()

    def RecieveInput(self,inputData):
        self.InputLayer = inputData

    def CalculateLayers(self):
        for cnt,_ in enumerate(self.HiddenLayers):
            if( cnt == 0):
                for curNode,_ in enumerate(self.HiddenLayers[cnt]):
                    Value = self.Biases[cnt][curNode]
                    for node,_ in enumerate(self.InputLayer):
                        Value += node * self.Weights[cnt][curNode][node]
                    self.HiddenLayers[cnt][curNode] = Value
            else:
                for curNode,_ in enumerate(self.HiddenLayers[cnt]):
                    Value = self.Biases[cnt][curNode]
                    for node,_ in enumerate(self.HiddenLayers[cnt-1]):
                        Value += node * self.Weights[cnt][curNode][node]
                    self.HiddenLayers[cnt][curNode] = self.getSigmoid(Value)
    
    def getSigmoid(self,inputVal):
        return 1/1+exp(-inputVal)

    def printWeights(self):
        with open("weights.csv","w") as file:
            writer = csv.writer(file)

            for cnt,row in enumerate(self.Weights):
                tempArray = [cnt + 1]
                for x in row:
                    tempArray.append(x)
                writer.writerow(tempArray)
    
    def printOutput(self):
        with open("Output.csv","w") as file:
            writer = csv.writer(file)

            for cnt,row in enumerate(Bots.HiddenLayers[-1]):
                writer.writerow([cnt + 1, row])

    
Bots = DameBot("c1",3, [12,10,10],True)

Bots.RandomizeChange(2)

Bots.RecieveInput([1] * 64)
Bots.CalculateLayers()
Bots.printOutput()

selectedOutput = Bots.HiddenLayers[-1].index(max(Bots.HiddenLayers[-1]))

print(selectedOutput)