from Robot import *
from operator import itemgetter



def initGeneration(n):
    generation = []
    for i in range(n):
        battery = rand.randint(1, 3)
        motor = rand.randint(1, 3)
        camera = 1
        behaviour = createRandomMarkovChain()
        robot = Robot(battery, motor, camera, behaviour, None, None)
        generation.append(robot)
    return generation



def adaptability(robot):
    # Distance to exit: 50%
    # param = 38 - <rows and columns of difference to exit>
    # param = % -> 38 = 50%

    # Cost: 25%
    # param = 700 - <cost>
    # param = % -> 400 = 25%

    # Time (Moves taken, applies only if maze is solved): 25%
    # param = 90 - <moves taken>
    # param = % -> 90 = 25%
    #
    # The minimum value of adaptability is 0.1
    adaptabilityValue = 0.0
    if robot.position[0] != SIZE - 1 or robot.position[1] != 0:
        difference = robot.position[0] + ((SIZE - 1) - robot.position[1])
        adaptabilityValue += ((38 - difference) * 50) / 38
    if robot.cost != 700:
        adaptabilityValue += ((700 - robot.cost) * 25) / 400
    if robot.position[0] == 0 and robot.position[1] == SIZE - 1:
        if robot.moves != 90:
            adaptabilityValue += ((90 - robot.moves) * 25) / 90
    if adaptabilityValue == 0.0:
        adaptabilityValue = 0.1
    robot.adaptability = adaptabilityValue


def selection(generation, crossoverIndividuals):
    selected = []
    relativeAdaptabilities = []
    totalAdaptability = 0.0
    totalRelativeAdaptability = 0.0
    for robot in generation:
        adaptability(robot)
        totalAdaptability += robot.adaptability
    avarageAdaptability = totalAdaptability / len(generation)
    for robot in generation:
        robot.relativeAdaptability = (robot.adaptability / avarageAdaptability) / len(generation)
        relativeAdaptabilities.append((robot, robot.relativeAdaptability))
        totalRelativeAdaptability += robot.relativeAdaptability
    relativeAdaptabilities.sort(key=itemgetter(1))
    for i in range(crossoverIndividuals):
        probability = rand.uniform(0, totalRelativeAdaptability)
        accumulatedProbability = 0.0
        for tuple in relativeAdaptabilities:
            if accumulatedProbability <= probability < tuple[1] + accumulatedProbability:
                selected.append(tuple[0])
                break
            else:
                accumulatedProbability += tuple[1]
    return selected

def crossover (selected):
    pass