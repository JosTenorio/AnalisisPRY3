from GeneticSelector import *
from GUI import *
import sys

def pathSolver():
    global INITIAL_POPULATION, MUTATION_PROBABILITY_HARDWARE, MUTATION_PROBABILITY_BEHAVIOUR, GEN_COUNT, GEN_ARCHIVE, GEN_NUMBERS, ADAPTABILITY_ARCHIVE, RUNNING, GRAPH, SELECTED_GEN_INDEX, SELECTED_ROBOT
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
    SELECTED_GEN_INDEX = GEN_COUNT - 1
    SELECTED_ROBOT = GEN_ARCHIVE[SELECTED_GEN_INDEX][SELECTED_ROB_INDEX]

def start():
    global GEN_COUNT, GEN_ARCHIVE, GEN_NUMBERS, ADAPTABILITY_ARCHIVE, GRAPH, RUNNING, SELECTED_ROB_INDEX, SELECTED_GEN_INDEX, SELECTED_ROBOT
    GEN_COUNT = 0
    GEN_ARCHIVE = []
    GEN_NUMBERS = []
    ADAPTABILITY_ARCHIVE = []
    GRAPH = None
    SELECTED_ROB_INDEX = 0
    SELECTED_GEN_INDEX = 0
    SELECTED_ROBOT = None
    RUNNING = True
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
SELECTED_ROB_INDEX = 0
SELECTED_GEN_INDEX = 0
SELECTED_ROBOT = None
RUNNING = True

# thread setup
solverThread = threading.Thread(target = pathSolver, daemon = True)

# buttons
startButton = Button(COLOR_BROWN, 250, 30, 80, 40, 20, "START")
stopButton = Button(COLOR_BROWN, 250, 90, 80, 40, 20, "STOP")
cycleButton = Button(COLOR_BROWN, 850, 40, 180, 40, 20, "CYCLE GENERATION")
parent1Button = Button(COLOR_BROWN, 850, 100, 180, 40, 20, "PARENT 1")
parent2Button = Button(COLOR_BROWN, 850, 160, 180, 40, 20, "PARENT 2")

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
            elif cycleButton.isOver(pos):
                if not RUNNING and SELECTED_ROBOT is not None:
                    if SELECTED_ROB_INDEX + 1 >= len(GEN_ARCHIVE[SELECTED_GEN_INDEX]):
                        SELECTED_ROB_INDEX = 0
                    else:
                        SELECTED_ROB_INDEX += 1
                    SELECTED_ROBOT = GEN_ARCHIVE[SELECTED_GEN_INDEX][SELECTED_ROB_INDEX]
            elif parent1Button.isOver(pos):
                if not RUNNING and SELECTED_ROBOT is not None:
                    if SELECTED_GEN_INDEX - 1 >= 0:
                        SELECTED_GEN_INDEX -= 1
                        SELECTED_ROBOT = SELECTED_ROBOT.parents[0]
            elif parent2Button.isOver(pos):
                if not RUNNING and SELECTED_ROBOT is not None:
                    if SELECTED_GEN_INDEX - 1 >= 0:
                        SELECTED_GEN_INDEX -= 1
                        SELECTED_ROBOT = SELECTED_ROBOT.parents[1]

    WINDOW.fill(COLOR_CREAM)

    drawMatrix(MAP, 30, 30, 10)
    startButton.draw(COLOR_BLACK)
    stopButton.draw(COLOR_BLACK)

    if GRAPH is not None:
        WINDOW.blit(GRAPH, (630, 250))

    bestRobot = getBestRobot()
    if bestRobot is not None:
        drawText("BEST RESULT:", 20, 250, 150)
        drawMatrix(bestRobot.progressMap, 30, 250, 25)
        infoHardware = bestRobot.getInfoHardware()
        infoAdaptability = bestRobot.getInfoAdaptability()
        drawText(infoHardware, 20, 250, 180)
        drawText(infoAdaptability, 20, 250, 210)

    if not RUNNING and SELECTED_ROBOT is not None:
        cycleButton.draw(COLOR_BLACK)
        parent1Button.draw(COLOR_BLACK)
        parent2Button.draw(COLOR_BLACK)
        drawMatrix(SELECTED_ROBOT.progressMap, 1050, 30, 10)

    py.display.flip()
    CLOCK.tick(60)