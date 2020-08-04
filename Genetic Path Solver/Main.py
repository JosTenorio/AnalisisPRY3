from GeneticSelector import *

# Globals

# (Parameters)
INITIAL_POPULATION = 50
GENERATIONS = 5
INDIVIDUALS_PER_CROSSOVER = 6

# (Records)
Generations = []


#Main function
def geneticAlgorithm (initialPopulation, generations, crossoverIndividuals):
    for i in range(generations):
        currentGeneration = []
        previousGeneration = []
        if i == 0:
            currentGeneration = initGeneration(initialPopulation)
        else:
            previousGeneration = Generations[i-1]
            # Generar currentGeneration a partir del cruce
            #
            #
            #
            #
            #
            currentGeneration = initGeneration(initialPopulation)
        for robot in currentGeneration:
            robot.start()
        for robot in currentGeneration:
            robot.join()
        Generations.append(currentGeneration)

#Main program
geneticAlgorithm(INITIAL_POPULATION,GENERATIONS,INDIVIDUALS_PER_CROSSOVER)