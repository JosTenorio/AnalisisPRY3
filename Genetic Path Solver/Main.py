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
        if i == 0:
            currentGeneration = initGeneration(initialPopulation)
        else:
            selected = selection(Generations[i-1], crossoverIndividuals)
            # Generar currentGeneration a partir de selected (individuos seleccionados)
        for robot in currentGeneration:
            robot.start()
        for robot in currentGeneration:
            robot.join()
        Generations.append(currentGeneration)

#Main program