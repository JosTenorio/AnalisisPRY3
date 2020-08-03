import random
from Robot import *

def initPopulation(n):
    for i in range(n):
        battery = random.randint(1, 3)
        motor = random.randint(1, 3)
        camera = 1
        behaviour = createRandomMarkovChain()
        robot = Robot(battery, motor, camera, behaviour)

# globals
INITIAL_POPULATION = 1

initPopulation(INITIAL_POPULATION)