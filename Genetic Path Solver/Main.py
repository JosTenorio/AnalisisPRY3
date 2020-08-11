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

# Globals
GEN_COUNT = 0
GEN_ARCHIVE = []
GEN_NUMBERS = []
ADAPTABILITY_ARCHIVE = []
GRAPH = None
SELECTED_ROB_INDEX = 0
SELECTED_GEN_INDEX = 0
SELECTED_ROBOT = None
RUNNING = True

# parameters
INITIAL_POPULATION = 50
MUTATION_PROBABILITY_HARDWARE = 0.0
MUTATION_PROBABILITY_BEHAVIOUR = 0.0

# thread setup
solverThread = threading.Thread(target = pathSolver, daemon = True)

# buttons
startButton = Button(COLOR_BROWN, 250, 30, 80, 40, 20, "START")
stopButton = Button(COLOR_BROWN, 250, 90, 80, 40, 20, "STOP")
cycleButton = Button(COLOR_BROWN, 650, 15, 180, 40, 20, "CYCLE GENERATION")
parent1Button = Button(COLOR_BROWN, 650, 75, 180, 40, 20, "PARENT 1")
parent2Button = Button(COLOR_BROWN, 650, 135, 180, 40, 20, "PARENT 2")
childButton = Button(COLOR_BROWN, 650, 195, 180, 40, 20, "CHILD")

while True:

    for event in py.event.get():

        if event.type == py.QUIT:
            sys.exit()

        if event.type == py.MOUSEBUTTONDOWN:
            pos = py.mouse.get_pos()
            if startButton.isOver(pos):
                solverThread.start()
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
        childButton.draw(COLOR_BLACK)
        drawMatrix(SELECTED_ROBOT.progressMap, 850, 30, 10)
        infoHardware1 = SELECTED_ROBOT.getInfoHardwareSmall1()
        infoHardware2 = SELECTED_ROBOT.getInfoHardwareSmall2()
        infoAdaptability1 = SELECTED_ROBOT.getInfoAdaptabilitySmall1()
        infoAdaptability2 = SELECTED_ROBOT.getInfoAdaptabilitySmall2()
        drawText(infoHardware1, 20, 1070, 30)
        drawText(infoHardware2, 20, 1070, 60)
        drawText(infoAdaptability1, 20, 1070, 90)
        drawText(infoAdaptability2, 20, 1070, 120)

    py.display.flip()
    CLOCK.tick(60)