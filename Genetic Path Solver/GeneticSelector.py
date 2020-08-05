from Robot import *
from operator import itemgetter



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
    # 0 = 25%
    adaptability = 0.0
    if robot.position[0] != SIZE - 1 or robot.position[1] != 0:
        difference = robot.position[0] + ((SIZE - 1) - robot.position[1])
        adaptability += ((38 - difference) * 50) / 38
    if robot.cost != 700:
        adaptability += ((700 - robot.cost) * 25) / 400
    if robot.position[0] == 0 and robot.position[1] == SIZE - 1:
        if robot.moves != 90:
            adaptability += ((90 - robot.moves) * 25) / 90
    robot.adaptability = adaptability
    return adaptability


def selection(generation, crossoverIndividuals):
    selected = []
    adaptabilities = []
    totalAdaptability = 0.0
    for robot in generation:
        adaptability(robot)
        totalAdaptability += robot.adaptability
    avarageAdaptability = totalAdaptability / len(generation)
    for robot in generation:
        robot.adaptability = (robot.adaptability / avarageAdaptability) / len(generation)
        adaptabilities.append(tuple(robot, robot.adaptability))
    adaptabilities.sort(key=itemgetter(1))
    for i in range(crossoverIndividuals):
        probability = rand.uniform(0, 1)
        accumulatedProbability = 0.0
        for tuple in adaptabilities:
            if accumulatedProbability <= probability < tuple[1] + accumulatedProbability:
                selected.append(tuple[0])
                break
            else:
                accumulatedProbability += tuple[1]
    return selected


