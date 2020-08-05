from GeneticSelector import *

# Globals

# (Parameters)
INITIAL_POPULATION = 10
GENERATIONS = 2
INDIVIDUALS_PER_CROSSOVER = 3

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
            currentGeneration = selected #Generar la generacion nueva (currentGeneration) a partir de los seleccionados
        if i != generations - 1:
            for robot in currentGeneration:
                robot.start()
            for robot in currentGeneration:
                robot.join()
        Generations.append(currentGeneration)

#Main program
geneticAlgorithm (INITIAL_POPULATION, GENERATIONS, INDIVIDUALS_PER_CROSSOVER)
