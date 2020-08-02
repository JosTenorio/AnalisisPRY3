import threading
from MarkovChain import *

# globals
ENERGY_COST = [0, 1, 2, 3]
MAP = np.loadtxt("Terrain.txt", dtype='i', delimiter=',')

class Robot(threading.Thread):

    def __init__(self, battery, motor, camera, behaviour):
        threading.Thread.__init__(self)
        self.isRunning = True
        self.position = [19, 0]
        self.battery = battery
        self.motor = motor
        self.camera = camera
        self.behaviour = behaviour
        self.batteryLeft = (battery * 60)
        self.cost = (battery * 100) + (motor * 100) + (camera * 100)
        self.progressMap = np.copy(MAP)
        self.progressMap[self.position[0], self.position[1]] = 5
        self.printInfo()

    def move(self, moveX, moveY):
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
        self.printInfo()

    def run(self):
        pass

    def printInfo(self):
        print(self.progressMap)
        print("Motor:", self.motor, "Battery:", self.battery, "Remaining:", self.batteryLeft, "Camera:", self.camera)