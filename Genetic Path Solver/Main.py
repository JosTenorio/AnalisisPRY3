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
        print("NEXT GEN")
        print()
        for robot in gen:
            robot.printInfo()

# Globals
INITIAL_POPULATION = 20
GENERATIONS = 100
ARCHIVE = []

mazeSolver()
