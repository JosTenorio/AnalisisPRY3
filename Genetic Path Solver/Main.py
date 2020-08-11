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
    reset()

def reset():
    print("settings reset")

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

# buttons
startButton = Button(COLOR_BROWN, 250, 30, 80, 40, 20, "START")
stopButton = Button(COLOR_BROWN, 250, 90, 80, 40, 20, "STOP")

while True:

    for event in py.event.get():

        if event.type == py.QUIT:
            sys.exit()

        if event.type == py.MOUSEBUTTONDOWN:
            pos = py.mouse.get_pos()
            if startButton.isOver(pos):
                start()
            elif stopButton.isOver(pos):
                RUNNING = False

    WINDOW.fill(COLOR_CREAM)

    drawMatrix(MAP, 30, 30, 10)

    startButton.draw(COLOR_BLACK)
    stopButton.draw(COLOR_BLACK)

    drawText("BEST RESULT:", 20, 250, 150)

    if GRAPH is not None:
        WINDOW.blit(GRAPH, (630, 250))

    bestRobot = getBestRobot()
    if bestRobot is not None:
        drawMatrix(bestRobot.progressMap, 30, 250, 25)
        infoHardware = bestRobot.getInfoHardware()
        infoAdaptability = bestRobot.getInfoAdaptability()
        drawText(infoHardware, 20, 250, 180)
        drawText(infoAdaptability, 20, 250, 210)

    py.display.flip()
    CLOCK.tick(60)