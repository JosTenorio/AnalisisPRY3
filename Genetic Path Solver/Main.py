from GeneticSelector import *

def mazeSolver():
    global INITIAL_POPULATION, MUTATION_PROBABILITY, GEN_COUNT, ARCHIVE, ADAPTABILITY_RECORD
    currentGeneration = initGeneration(INITIAL_POPULATION)
    for i in range(GENERATIONS):
        for robot in currentGeneration:
            robot.start()
        for robot in currentGeneration:
            robot.join()
        totalAdaptability = evaluate(currentGeneration)
        ADAPTABILITY_RECORD.append(totalAdaptability)
        ARCHIVE.append(currentGeneration)
        GEN_COUNT += 1
        if i < GENERATIONS - 1:
            currentGeneration = crossGeneration(currentGeneration, totalAdaptability, MUTATION_PROBABILITY)
    for robot in currentGeneration:
        robot.printInfo()

# Globals
INITIAL_POPULATION = 20
GENERATIONS = 50 # change to while true
MUTATION_PROBABILITY = 0.0
GEN_COUNT = 0
ARCHIVE = []
ADAPTABILITY_RECORD = []

mazeSolver()