import threading
import pprint as pp
from random import *
from MarkovChain import *

# globals
ENERGY_COST = [0, 1, 2, 3]
MAP = np.loadtxt("Terrain.txt", dtype = 'i', delimiter = ',')

class Robot(threading.Thread):

    def __init__(self, battery, motor, camera, behaviour):
        threading.Thread.__init__(self)
        self.isRunning = True
        self.position = [SIZE - 1, 0]
        self.battery = battery
        self.motor = motor
        self.camera = camera
        self.behaviour = behaviour
        self.batteryLeft = (battery * 60)
        self.cost = (battery * 100) + (motor * 100) + (camera * 100)
        self.progressMap = np.copy(MAP)
        self.progressMap[self.position[0], self.position[1]] = 5
        self.printInfo()
        self.currentNode = self.getNodeCode(self.position[0], self.position[1], 4)

    def move(self, moveX, moveY, newNode):
        x = self.position[0]
        y = self.position[1]
        movementCost = ENERGY_COST[MAP[x, y]]
        if movementCost > self.batteryLeft:
            self.batteryLeft = 0
            self.isRunning = False
        else:
            self.batteryLeft -= movementCost
            self.position[0] += moveX
            self.position[1] += moveY
            self.progressMap[self.position[0], self.position[1]] = 5
            self.currentNode = newNode
        self.printInfo()

    def run(self):
        possible_nodes = self.getNextNodes()
        next_node = 0
        if len(possible_nodes) == 1:
            next_node = possible_nodes[0]
        else:
            possible_nodes = sorted(possible_nodes)
            probabilities_sum = 0
            for node in possible_nodes:
                probabilities_sum += self.behaviour[self.currentNode][node]
            random_float = random.uniform(0, probabilities_sum)
            accumulated_probability = 0
            for i in range(0, len(possible_nodes)):
                if random_float in range(accumulated_probability, self.behaviour[self.currentNode][possible_nodes[i]]):
                    next_node = possible_nodes[i]
                    break
                else:
                    accumulated_probability += self.behaviour[self.currentNode][possible_nodes[i]]
        direction = next_node % 10
        if direction == 1:
            self.move(0, 1, next_node)
        elif direction == 2:
            self.move(0, -1, next_node)
        elif direction == 3:
            self.move(1, 0, next_node)
        else:
            self.move(-1, 0, next_node)
        pass

    def printInfo(self):
        print(self.progressMap)
        print("Motor:", self.motor, "Battery:", self.battery, "Remaining:", self.batteryLeft, "Camera:", self.camera)

    def printMarkovChain(self):
        pp.pprint(self.behaviour)

    def getNextNodes(self):
        x = self.position[0]
        y = self.position[1]
        nodes = []
        if y - 1 >= 0:
            nodes += self.getNodeCode(x, y - 1, 1)
        if y + 1 < SIZE:
            nodes += self.getNodeCode(x, y + 1, 2)
        if x - 1 >= 0:
            nodes += self.getNodeCode(x - 1, y, 3)
        if x + 1 < SIZE:
            nodes += self.getNodeCode(x + 1, y, 4)
        return nodes

    def getNodeCode(self, x, y, direction):
        terrain = MAP[x, y]
        if terrain != 0 and terrain <= self.motor:
            return [direction + (self.battery * 10) + (self.motor * 100) + (terrain * 1000)]