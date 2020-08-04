import threading
import pprint as pp
import random as rand
from MarkovChain import *

# globals
ENERGY_COST = [0, 1, 2, 3]
MAP = np.loadtxt("Terrain.txt", dtype = 'i', delimiter = ',')
SIZE = len(MAP)

class Robot(threading.Thread):

    def __init__(self, battery, motor, camera, behaviour):
        threading.Thread.__init__(self)
        self.isRunning = True
        self.position = [SIZE - 1, 0]
        self.battery = battery
        self.motor = motor
        self.camera = camera
        self.behaviour = behaviour
        self.batteryLeft = (battery * 6) #60
        self.cost = (battery * 100) + (motor * 100) + (camera * 100)
        self.progressMap = np.copy(MAP)
        self.progressMap[self.position[0], self.position[1]] = 5
        self.currentNode = self.getNodeCode(self.position[0], self.position[1], 4)
        self.printInfo()

    def move(self, moveRow, moveCol, newNode):
        row = self.position[0]
        col = self.position[1]
        movementCost = ENERGY_COST[MAP[row, col]]
        if movementCost > self.batteryLeft:
            self.batteryLeft = 0
            self.isRunning = False
        else:
            self.batteryLeft -= movementCost
            self.position[0] += moveRow
            self.position[1] += moveCol
            self.progressMap[self.position[0], self.position[1]] = 5
            self.currentNode = newNode
            if self.batteryLeft == 0 or (self.position[0] == 0 and self.position[1] == SIZE - 1):
                self.isRunning = False
        self.printInfo()

    def run(self):
        while self.isRunning:
            possibleNodes = self.getNextNodes()
            print(possibleNodes)
            nextNode = None
            if len(possibleNodes) == 1:
                nextNode = possibleNodes[0]
            else:
                markovChain = self.behaviour[self.currentNode]
                possibleNodes = sorted(possibleNodes)
                probabilitySum = 0
                for node in possibleNodes:
                    probabilitySum += markovChain[node]
                randomFloat = rand.uniform(0, probabilitySum)
                accumulatedProbability = 0
                print (probabilitySum)
                print (randomFloat)
                for node in possibleNodes:
                    if accumulatedProbability <= randomFloat < markovChain[node] + accumulatedProbability:
                        nextNode = node
                        break
                    else:
                        accumulatedProbability += markovChain[node]
            if nextNode is not None:
                direction = nextNode % 10
                print("Direction", direction)
                if direction == 1:
                    self.move(-1, 0, nextNode)
                elif direction == 2:
                    self.move(1, 0, nextNode)
                elif direction == 3:
                    self.move(0, -1, nextNode)
                else:
                    self.move(0, 1, nextNode)
            else:
                print("NO NODE PICKED")


    def printInfo(self):
        print(self.progressMap)
        print("Motor:", self.motor, "Battery:", self.battery, "Remaining:", self.batteryLeft, "Camera:", self.camera)
        print()

    def printMarkovChain(self):
        pp.pprint(self.behaviour)
        print()

    def getNextNodes(self):
        row = self.position[0]
        col = self.position[1]
        nodes = []
        if row - 1 >= 0:
            code = self.getNodeCode(row - 1, col, 1)
            if code is not None:
                nodes += code
        if row + 1 < SIZE:
            code = self.getNodeCode(row + 1, col, 2)
            if code is not None:
                nodes += code
        if col - 1 >= 0:
            code = self.getNodeCode(row, col - 1, 3)
            if code is not None:
                nodes += code
        if col + 1 < SIZE:
            code = self.getNodeCode(row, col + 1, 4)
            if code is not None:
                nodes += code
        return nodes

    def getNodeCode(self, row, col, direction):
        terrain = MAP[row, col]
        if terrain != 0 and terrain <= self.motor:
            return [direction + (self.battery * 10) + (self.motor * 100) + (terrain * 1000)]
        return None