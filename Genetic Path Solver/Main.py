from GeneticSelector import *
from GUI import *
import sys

def pathSolver():
    global INITIAL_POPULATION, MUTATION_PROBABILITY_HARDWARE, MUTATION_PROBABILITY_BEHAVIOUR, GEN_COUNT, GEN_ARCHIVE, GEN_NUMBERS, ADAPTABILITY_ARCHIVE, RUNNING, GRAPH
    currentGeneration = initGeneration(INITIAL_POPULATION)
    while RUNNING:
        for robot in currentGeneration:
            robot.start()
        for robot in currentGeneration:
            robot.join()
        totalAdaptability = evaluate(currentGeneration)
        ADAPTABILITY_ARCHIVE.append(totalAdaptability)
        GEN_ARCHIVE.append(currentGeneration)
        GEN_COUNT += 1
        GEN_NUMBERS.append(GEN_COUNT)
        GRAPH = plot(GEN_NUMBERS, ADAPTABILITY_ARCHIVE, "b")
        if RUNNING:
            currentGeneration = crossGeneration(currentGeneration, totalAdaptability, MUTATION_PROBABILITY_HARDWARE, MUTATION_PROBABILITY_BEHAVIOUR)

def reset():
    pass

def start():
    solverThread.start()

# Globals
INITIAL_POPULATION = 50
MUTATION_PROBABILITY_HARDWARE = 0.0
MUTATION_PROBABILITY_BEHAVIOUR = 0.0
GEN_COUNT = 0
GEN_ARCHIVE = []
GEN_NUMBERS = []
ADAPTABILITY_ARCHIVE = []
GRAPH = None
RUNNING = True

# thread setup
solverThread = threading.Thread(target = pathSolver, daemon = True)
start()

while True:

    for event in py.event.get():

        if event.type == py.QUIT:
            sys.exit()

    WINDOW.fill(COLOR_CREAM)

    drawMatrix(MAP, 30, 30, 10)

    if GRAPH is not None:
        WINDOW.blit(GRAPH, (630, 250))

    bestRobot = getBestRobot()
    if bestRobot is not None:
        drawMatrix(bestRobot.progressMap, 30, 250, 25)

    py.display.flip()
    CLOCK.tick(60)