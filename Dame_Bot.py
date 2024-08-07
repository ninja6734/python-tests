from random import *
import csv
from math import *
import tkinter

class DameBot:
    type = ""
    InputLayer = []
    HiddenLayers = []
    Weights = []
    Biases = []
    randMinVal = 0
    randMaxVal = 0
    _input = 0
    pID = 0
    cost = 0

    #initialisation
    def __init__(self, type, HiddenLayerSize = 3, Nodes = [12,10,10], firstInit = False) -> None:
        self.cost = 0

        if(firstInit):
            self.Biases = []
            self.HiddenLayers = []
            self.Weights = []
            self.InputLayer = []
            self.pID = 0

        #throw error if input is wrong
        if(len(Nodes) != HiddenLayerSize):
            raise IndexError("Nodes must be the same length as the HiddenLayerSize minus the Ouput Layer (1)")
        self.type = type
        
        #Initialize HiddenLayer
        for i in range(HiddenLayerSize):
            self.HiddenLayers.append([0 for _ in range(Nodes[i])])
        self.HiddenLayers.append([0 for _ in range(4096)])

        #initialize InputLayer
        self.InputLayer = [0 for _ in range(64)]

        self.createWeightsBiases(HiddenLayerSize, Nodes)

        #init weight randomness
        if(firstInit):
            self.RandomizeInit()
        else:
            self.randomizeValue()

    def setID(self, id):
        self.pID = id

    
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
                        TempWeights.append([0 for _ in range(len(self.InputLayer))])
                    else:
                        TempWeights.append([0 for _ in range(Nodes[HiddenLayerNum - 1])])
            else:
                for _ in range(4096):
                    TempBiases.append(0)
                    TempWeights.append([0 for _ in range( Nodes[-1])])
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
                    self.HiddenLayers[cnt][curNode] = self.getActivation(Value)
    
    def getActivation(self,inputVal):
        if(inputVal > 1):
            return 1
        elif(inputVal < 0):
            return 0
        else:
            return inputVal

    def printWeights(self):
        with open("weights.csv","w") as file:
            writer = csv.writer(file)

            for cnt,row in enumerate(self.Weights):
                tempArray = [f"layer: {cnt + 1}"]
                for x in row:
                    tempArray.append(x)
                writer.writerow(tempArray)
    
    def printOutput(self):
        with open("Output.csv","w") as file:
            writer = csv.writer(file)

            for cnt,row in enumerate(self.HiddenLayers[-1]):
                writer.writerow([f"layer: {cnt + 1}", row])

    def getReaction(self,Data):
        self.RecieveInput([x for xs in Data for x in xs])
        self.CalculateLayers()
        return self.HiddenLayers[-1].index(max(self.HiddenLayers[-1]))
    
    def moveOnBoard(self,currentGame):
        reaction = self.getReaction(currentGame.Board)
        start = reaction % 64
        end = int((reaction - start) / 64)
        sx = start % 8
        sy = int((start - sx) / 8)
        ex = end % 8
        ey = int((end - ex) / 8)
        res = currentGame.doMove(sx,sy,ex,ey,self.pID)
        return res

class DameGame:
    Board = []
    Type = ""
    def __init__(self, type):
        self.Board = self.SetupGame()
        self.Type = type

    
    def SetupGame(self):
        Array = [[0 for _ in range(8)] for _ in range(8)]
        for rowCnt,_ in enumerate(Array):
            if(rowCnt < 3):
                if (rowCnt == 1):
                    Array[rowCnt] = [0,1,0,1,0,1,0,1]
                else:
                    Array[rowCnt] = [1,0,1,0,1,0,1,0]
            elif(rowCnt > 4):
                if(rowCnt == 6):
                    Array[rowCnt] = [0,-1,0,-1,0,-1,0,-1]
                else:
                    Array[rowCnt] = [-1,0,-1,0,-1,0,-1,0]

        return Array
    
    
    def showField(self):
        canvas.delete("all")
        for colNum,col in enumerate(self.Board):
            for rowNum,row in enumerate(col):
                if(colNum % 2 == 0):
                    if(rowNum % 2 != 0):
                        canvas.create_rectangle(30+rowNum * 40,350 - colNum * 40,70 + rowNum * 40,310 - colNum * 40,fill="green")
                else:
                    if(rowNum % 2 == 0):
                        canvas.create_rectangle(30+rowNum * 40,350 - colNum * 40,70 + rowNum * 40,310 - colNum * 40,fill="green")
                if(row == 1):
                    canvas.create_oval(30+rowNum * 40,350 - colNum * 40,70 + rowNum * 40,310 - colNum * 40,fill="blue")
                elif(row == -1):
                    canvas.create_oval(30+rowNum * 40,350 - colNum * 40,70 + rowNum * 40,310 - colNum * 40,fill="violet")

    
    def doMove(self,startX, startY, endX, endY, playerID):
        if(self.Board[startY][startX] == 0):
            return 5
        else:
            allowed = self.checkStart(startX, startY,playerID)
            if(allowed == 0):
                pick = self.Board[startY][startX]
                allowed = self.checkEnd(startX,startY,endX,endY,playerID)
                if(allowed == 0):
                    self.Board[startY][startX] = 0
                    self.Board[endY][endX] = pick
                    return 0
                elif(allowed == 1):
                    return 3
                elif(allowed == 2):
                    return 2
                else:
                    return 1
            else:
                return 4
    
    def checkStart(self,startX, startY, playerID):
        if(self.Board[startY][startX] == playerID):
            return 0
        else:
            return 1
        
    def checkEnd(self,startX,startY,endX,endY,pID):
        if(self.Board[endY][endX] == 0):
            if((endX - startX + endY - startY) % 2 == 0):
                if(startX == endX and startY == endY):
                    return 3
                else:
                    if(abs(endX - startX) < 2 and abs(endY - startY) < 2):
                        return 0
                    else:
                        allowed = self.checkRoute(startX,startY,endX,endY,pID)
                    if(allowed == 0):
                        return 0
                    else:
                        return 2
            else:
                return 2
        else:
            return 1
    
    def checkRoute(self,startX,startY,endX,endY,pID,Ways=[]):
        BoardCopy = self.Board
        FoundWays = Ways
        if(FoundWays != []):
            curX = FoundWays[0][0]
            curY = FoundWays[0][1]
        else:
            curX = startX
            curY = startY
        newWays = self.findWays(curX,curY,BoardCopy,pID)
        if(newWays != None):
            FoundWays.append(newWays)
        if([endX,endY] in FoundWays):
            return 0
        else:
            if(FoundWays == []):
                return 2
            else:
                self.checkRoute(startX,startY,endX,endY,pID,FoundWays)
    
    def findWays(self,posX,posY,boardCopy,pID):
        ways = []
        for off in [[1,1],[1,-1],[-1,-1],[-1,1]]:
            if(len(boardCopy)  > posY + off[0]):
                if(len(boardCopy[posY + off[0]]) > posX + off[1]):
                    if(boardCopy[posY  + off[0]][posX + off[1]] == -(pID)):
                        ways.append([posX + off[0] * 2, posY + off[1] * 2])
        if(ways !=  []):
            return ways
        else:
            return None

def checkWinner(currentGame):
    ones = 0
    neg_ones = 0
    for row in currentGame.Board:
        if(-1 in row):
            ones += 1
        elif(not 1 in row):
            neg_ones += 1
    
    if(ones == 0):
        return -1
    elif(neg_ones == 0):
        return 1
    else:
        return 0

def simulateGame(type, roundInterv, Bot1, Bot2):
    Game = DameGame(type)
    print(f"round this game: {roundInterv}")

    cnt = 0
    winner = 0
    while(cnt < roundInterv and winner == 0):
        cost = Bot1.moveOnBoard(Game)
        Bot1.cost += cost
        cost = Bot2.moveOnBoard(Game)
        Bot2.cost += cost
        cnt += 1
        winner = checkWinner(Game)

    print(cnt)

    if(winner == 0):
        winner = (int(Bot1.cost < Bot2.cost) * 2 - 1) 

    print(f"winner: {winner}")
    if(winner == 1):
        print(f"winner-cost: {Bot1.cost}")
        print(f"loser-cost: {Bot2.cost}")
    else:
        print(f"winner-cost: {Bot2.cost}")
        print(f"loser-cost: {Bot1.cost}")
    
    return [Bot1.cost, Bot2.cost, winner, cnt, Game.Board]

def simulateGameLoop(roundInterv):
    Bot1 = DameBot("Bot1",firstInit=True)
    Bot1.setID(1)
    Bot2 = DameBot("Bot2",firstInit=True)
    Bot2.setID(-1)
    rounds = 20

    for GameCnt in range(roundInterv):
        GameResult = simulateGame(f"Game {GameCnt+1}", rounds, Bot1, Bot2)
        Bot1Cost = GameResult[0] + int(GameResult[2] == -1) * 200
        Bot2Cost = GameResult[1] + int(GameResult[2] == 1) * 200
        Bot1.RandomizeChange(cost=Bot1Cost)
        Bot2.RandomizeChange(cost=Bot2Cost)
        rounds = 200


    
  
simulateGameLoop(100)