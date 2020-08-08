from GeneticSelector import *

def mazeSolver():
    currentGeneration = initGeneration(INITIAL_POPULATION)
    for i in range(GENERATIONS):
        for robot in currentGeneration:
            robot.start()
        for robot in currentGeneration:
            robot.join()
        ARCHIVE.append(currentGeneration)
        if i < GENERATIONS - 1:
            currentGeneration = crossGeneration(currentGeneration)
    printResults()

def printResults():
    for gen in ARCHIVE:
        for robot in gen:
            robot.printHardware()

# Globals
INITIAL_POPULATION = 1
GENERATIONS = 1
INDIVIDUALS_PER_CROSSOVER = 0
ARCHIVE = []

mazeSolver()
