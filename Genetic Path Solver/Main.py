import random as rand
from Robot import *

def initPopulation(n):
    for i in range(n):
        battery = rand.randint(1, 3)
        motor = rand.randint(1, 3)
        camera = 1
        behaviour = createRandomMarkovChain()
        robot = Robot(1, 1, 1, behaviour)
        robot.start()

# globals
INITIAL_POPULATION = 1

initPopulation(INITIAL_POPULATION)