import threading
import pprint as pp
import random as rand
from MarkovChain import *

# globals
ENERGY_COST = [0, 1, 2, 3]
MAP = np.loadtxt("Terrain.txt", dtype = 'i', delimiter = ',')
SIZE = len(MAP)
CAMERA_UNITS = 1
BATTERY_UNITS = 3
MOTOR_UNITS = 3
BATTERY_PER_UNIT = 50
COST_PER_HARDWARE = 100
HARDWARE_COMPONENTS = 3

class Robot(threading.Thread):

    def __init__(self, motor, battery, camera, behaviour, parent1, parent2):
        threading.Thread.__init__(self)
        self.isRunning = True
        self.position = [SIZE - 1, 0]
        self.motor = motor
        self.battery = battery
        self.camera = camera
        self.behaviour = behaviour
        self.batteryLeft = (battery * BATTERY_PER_UNIT)
        self.cost = (battery * COST_PER_HARDWARE) + (motor * COST_PER_HARDWARE) + (camera * COST_PER_HARDWARE)
        self.progressMap = np.copy(MAP)
        self.progressMap[self.position[0], self.position[1]] = 4
        self.currentNode = self.getNodeCode(self.position[0], self.position[1], 4)
        self.adaptability = 0.0
        self.relativeAdaptability = 0.0
        self.moves = 0
        self.parents = [parent1, parent2]

    def move(self, moveRow, moveCol, newNode):
        row = self.position[0]
        col = self.position[1]
        movementCost = ENERGY_COST[MAP[row, col]]
        if movementCost > self.batteryLeft:
            self.batteryLeft = 0
            self.isRunning = False
            self.progressMap[self.position[0], self.position[1]] = 5
        else:
            self.batteryLeft -= movementCost
            self.position[0] += moveRow
            self.position[1] += moveCol
            self.moves += 1
            self.currentNode = newNode
            self.progressMap[self.position[0], self.position[1]] = 4
            if self.batteryLeft == 0 or (self.position[0] == 0 and self.position[1] == SIZE - 1):
                self.isRunning = False
                self.progressMap[self.position[0], self.position[1]] = 5

    def run(self):
        while self.isRunning:
            possibleNodes = self.getNextNodes()
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
                for node in possibleNodes:
                    if accumulatedProbability <= randomFloat < markovChain[node] + accumulatedProbability:
                        nextNode = node
                        break
                    else:
                        accumulatedProbability += markovChain[node]
            direction = nextNode % 10
            if direction == 1:
                self.move(-1, 0, nextNode)
            elif direction == 2:
                self.move(1, 0, nextNode)
            elif direction == 3:
                self.move(0, -1, nextNode)
            else:
                self.move(0, 1, nextNode)

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

    def getInfoHardware(self):
        string = "Motor: " + str(self.motor) + " Battery: " + str(self.battery) + " Remaining: " + str(self.batteryLeft) + " Camera: " + str(self.camera)
        return string

    def getInfoAdaptability(self):
        string = "Moves: " + str(self.moves) + " Cost: " + str(self.cost) + " Adaptability " + str(round(self.adaptability, 2))
        return string

    def printInfo(self):
        print(self.progressMap)
        print("Motor:", self.motor, "Battery:", self.battery, "Remaining:", self.batteryLeft, "Camera:", self.camera)
        print("Moves:", self.moves, "Cost:", self.cost, "Adaptability:", self.adaptability, "Relative:", self.relativeAdaptability)
        print()

    def printMarkovChain(self):
        pp.pprint(self.behaviour)
        print()

    def getInfoHardwareSmall1(self):
        string = "Motor: " + str(self.motor) + " Battery: " + str(self.battery)
        return string

    def getInfoHardwareSmall2(self):
        string = "Remaining: " + str(self.batteryLeft) + " Camera: " + str(self.camera)
        return string

    def getInfoAdaptabilitySmall1(self):
        string = "Moves: " + str(self.moves) + " Cost: " + str(self.cost)
        return string

    def getInfoAdaptabilitySmall2(self):
        string = "Adaptability " + str(round(self.adaptability, 2))
        return string