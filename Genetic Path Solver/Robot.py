import numpy as np

# globals
MAP = np.loadtxt("Terrain.txt", dtype='i', delimiter=',')
ENERGY_COST = [0, 1, 2, 3]

class Robot:

    def __init__(self, battery, motor, camera, behaviour):
        self.isRunning = True
        self.position = [19, 0]
        self.battery = battery
        self.motor = motor
        self.camera = camera
        self.behaviour = behaviour
        self.batteryLeft = (battery * 60)
        self.cost = (battery * 100) + (motor * 100) + (camera * 100)

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