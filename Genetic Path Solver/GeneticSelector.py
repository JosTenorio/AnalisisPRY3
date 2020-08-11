from Robot import *
from operator import itemgetter

#globals
BEST_SCORE = 0
BEST_ROBOT = None

def getBestRobot():
    return BEST_ROBOT

def initGeneration(n):
    generation = []
    for i in range(n):
        motor = rand.randint(1, MOTOR_UNITS)
        battery = rand.randint(1, BATTERY_UNITS)
        camera = rand.randint(1, CAMERA_UNITS)
        behaviour = createRandomMarkovChain()
        robot = Robot(motor, battery, camera, behaviour, None, None)
        generation.append(robot)
    rand.shuffle(NODES)
    return generation

def adaptability(robot):
    adaptabilityValue = 0.0
    maxCost = COST_PER_HARDWARE * (BATTERY_UNITS + MOTOR_UNITS + CAMERA_UNITS)
    minCost = COST_PER_HARDWARE * HARDWARE_COMPONENTS
    maxMoves = BATTERY_PER_UNIT * BATTERY_UNITS
    maxDiference = (SIZE - 1) * 2
    positionValue = 60
    costValue = 20
    timeValue = 20
    if robot.position[0] != SIZE - 1 and robot.position[1] != 0:
        difference = robot.position[0] + ((SIZE - 1) - robot.position[1])
        adaptabilityValue += ((maxDiference - difference) * positionValue) / maxDiference
        if adaptabilityValue > positionValue / 2:
            if robot.cost < maxCost:
                adaptabilityValue += ((maxCost - robot.cost) * costValue) / minCost
    if robot.position[0] == 0 and robot.position[1] == SIZE - 1:
        if robot.moves < maxMoves:
            adaptabilityValue += ((maxMoves - robot.moves) * timeValue) / maxMoves
    if adaptabilityValue == 0.0:
        adaptabilityValue = 0.1
    robot.adaptability = adaptabilityValue

def evaluate(generation):
    global BEST_SCORE, BEST_ROBOT
    totalAdaptability = 0.0
    for robot in generation:
        adaptability(robot)
        if robot.adaptability > BEST_SCORE:
            BEST_SCORE = robot.adaptability
            BEST_ROBOT = robot
        totalAdaptability += robot.adaptability
    return totalAdaptability

def selection(generation, totalAdaptability):
    selected = []
    relativeAdaptabilities = []
    population = len(generation)
    totalRelativeAdaptability = 0.0
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

def crossGeneration(generation, totalAdaptability, mutationProbabilityHardware, mutationProbabilityBehaviour):
    newGeneration = []
    selected = selection(generation, totalAdaptability)
    rand.shuffle(selected)
    for i in range(0, len(selected), 2):
        robotMale = selected[i]
        maleGenes = [robotMale.motor, robotMale.battery, robotMale.camera, robotMale.behaviour]
        if i + 1 >= len(selected):
            robotFemale = selected[0]
        else:
            robotFemale = selected[i + 1]
        femaleGenes = [robotFemale.motor, robotFemale.battery, robotFemale.camera, robotFemale.behaviour]
        crossHardware(maleGenes, femaleGenes, mutationProbabilityHardware)
        crossMarkovChain(maleGenes[3], femaleGenes[3], mutationProbabilityBehaviour)
        newGeneration.append(Robot(maleGenes[0], maleGenes[1], maleGenes[2], maleGenes[3], robotMale, robotFemale))
        newGeneration.append(Robot(femaleGenes[0], femaleGenes[1], femaleGenes[2], femaleGenes[3], robotMale, robotFemale))
    return newGeneration

def crossHardware(maleGenes, femaleGenes, mutationProbability):
    crossPoint = rand.randint(0, HARDWARE_COMPONENTS - 1)
    for j in range(crossPoint):
        swap = maleGenes[j]
        maleGenes[j] = femaleGenes[j]
        femaleGenes[j] = swap
    mutateHardware(maleGenes, mutationProbability)
    mutateHardware(femaleGenes, mutationProbability)
    
def mutateHardware(genes, mutationProbability):
    prob = rand.uniform(0, 1)
    if prob < mutationProbability:
        mutation = rand.randint(0, HARDWARE_COMPONENTS - 1)
        if mutation == 0:
            genes[mutation] = rand.randint(1, MOTOR_UNITS)
        elif mutation == 1:
            genes[mutation] = rand.randint(1, BATTERY_UNITS)
        elif mutation == 2:
            genes[mutation] = rand.randint(1, CAMERA_UNITS)

def crossMarkovChain(maleChain, femaleChain, mutationProbability):
    crossPoint = rand.randint(1, NODE_AMOUNT - 1)
    for i in range(crossPoint):
        swap = maleChain[NODES[i]]
        maleChain[NODES[i]] = femaleChain[NODES[i]]
        femaleChain[NODES[i]] = swap
    mutateMarkovChain(maleChain, mutationProbability)
    mutateMarkovChain(femaleChain, mutationProbability)

def mutateMarkovChain(chain, mutationProbability):
    prob = rand.uniform(0, 1)
    if prob < mutationProbability:
        mutation = rand.choice(NODES)
        values = sumToX(NODE_AMOUNT, 1)
        counter = 0
        for nextNode in NODES:
            chain[mutation][nextNode] = values[counter]
            counter += 1