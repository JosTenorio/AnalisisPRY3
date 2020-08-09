from Robot import *
from operator import itemgetter

def initGeneration(n):
    generation = []
    for i in range(n):
        motor = rand.randint(1, MOTOR_UNITS)
        battery = rand.randint(1, BATTERY_UNITS)
        camera = rand.randint(1, CAMERA_UNITS)
        behaviour = createRandomMarkovChain()
        robot = Robot(motor, battery, camera, behaviour, None, None)
        generation.append(robot)
    return generation

# Distance to exit: 50%
# param = 38 - <rows and columns of difference to exit>
# param = % -> 38 = 50%

# Cost: 25%
# param = 700 - <cost>
# param = % -> 300 = 25%

# Time (Moves taken, applies only if maze is solved): 25%
# param = 90 - <moves taken>
# param = % -> 90 = 25%

# The minimum value of adaptability is 0.1

def adaptability(robot):
    adaptabilityValue = 0.0
    maxCost = COST_PER_HARDWARE * (BATTERY_UNITS + MOTOR_UNITS + CAMERA_UNITS)
    minCost = COST_PER_HARDWARE * HARDWARE_COMPONENTS
    maxMoves = BATTERY_PER_UNIT * BATTERY_UNITS
    minMoves = BATTERY_PER_UNIT * max(ENERGY_COST)
    if robot.position[0] != SIZE - 1 and robot.position[1] != 0:
        difference = robot.position[0] + ((SIZE - 1) - robot.position[1])
        adaptabilityValue += ((38 - difference) * 50) / 38
    if robot.cost < maxCost:
        adaptabilityValue += ((maxCost - robot.cost) * 25) / minCost
    if robot.position[0] == 0 and robot.position[1] == SIZE - 1:
        if robot.moves < maxMoves:
            adaptabilityValue += ((maxMoves - robot.moves) * 25) / minMoves
    if adaptabilityValue == 0.0:
        adaptabilityValue = 0.1
    robot.adaptability = adaptabilityValue

def selection(generation):
    selected = []
    relativeAdaptabilities = []
    population = len(generation)
    totalAdaptability = 0.0
    totalRelativeAdaptability = 0.0
    for robot in generation:
        adaptability(robot)
        totalAdaptability += robot.adaptability
    avarageAdaptability = totalAdaptability / population
    for robot in generation:
        robot.relativeAdaptability = (robot.adaptability / avarageAdaptability) / population
        relativeAdaptabilities.append((robot, robot.relativeAdaptability))
        totalRelativeAdaptability += robot.relativeAdaptability
    relativeAdaptabilities.sort(key = itemgetter(1))
    for i in range(population):
        probability = rand.uniform(0, totalRelativeAdaptability)
        accumulatedProbability = 0.0
        for robotAdaptability in relativeAdaptabilities:
            if accumulatedProbability <= probability < robotAdaptability[1] + accumulatedProbability:
                selected.append(robotAdaptability[0])
                break
            else:
                accumulatedProbability += robotAdaptability[1]
    return selected

def crossGeneration(generation):
    newGeneration = []
    selected = selection(generation)
    rand.shuffle(selected)
    for i in range(0, len(selected), 2):
        robotMale = selected[i]
        maleGenes = [robotMale.motor, robotMale.battery, robotMale.camera, robotMale.behaviour]
        if i + 1 >= len(selected):
            robotFemale = selected[0]
        else:
            robotFemale = selected[i + 1]
        femaleGenes = [robotFemale.motor, robotFemale.battery, robotFemale.camera, robotFemale.behaviour]
        crossPoint = rand.randint(1, HARDWARE_COMPONENTS)
        for j in range(crossPoint):
            swap = maleGenes[j]
            maleGenes[j] = femaleGenes[j]
            femaleGenes[j] = swap
        newGeneration.append(Robot(maleGenes[0], maleGenes[1], maleGenes[2], maleGenes[3], robotMale, robotFemale))
        newGeneration.append(Robot(femaleGenes[0], femaleGenes[1], femaleGenes[2], femaleGenes[3], robotMale, robotFemale))
    return newGeneration
#mutation