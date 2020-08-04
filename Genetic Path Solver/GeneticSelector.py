from Robot import *
import math


def initGeneration(n):
    generation = []
    for i in range(n):
        battery = rand.randint(1, 3)
        motor = rand.randint(1, 3)
        camera = 1
        behaviour = createRandomMarkovChain()
        robot = Robot(battery, motor, camera, behaviour)
        generation.append(robot)
    return generation


#Adaptability:
#Distance to exit: 50%
# 0 = 50%, if robot is in entrance = 0%

#Cost: 25%
# 700 = 0%, 300 = 25%

#Time (Moves taken): 25%
# 0 = 25%


def adaptability (robot):
    adaptability = 0.0
    if robot.position[0] != SIZE -1 or robot.position[1] == 0:
        if robot.position[0] == 0 and robot.position[1] == SIZE - 1:
            adaptability += 50
        else:
            distanceToExit = math.sqrt()
    return adaptability





def selection (generation, crossoverIndividuals):
    populationLeft = generation
    adaptabilities = []
    selected = []
    for robot in generation:
        adaptability(robot)
        adaptabilities.append(robot.adaptability)
    for i in range(crossoverIndividuals):
        index = adaptabilities.index(max(adaptabilities))
        selected.append(populationLeft[index])
        populationLeft.pop(index)
        adaptabilities.pop(index)
    return selected


