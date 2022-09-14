import csv
import sys
import copy
import time
import random as r
import pandas as pd

AND = 0
OR = 1
XOR = 2
NAND = 3
NOR = 4
XNOR = 5

class Chromosome:
    def __init__(self):
        self.gene = []
        self.fitness = 0
    def print(self):
        counter = 1
        for i in self.gene:
            print("Gate %d:" % counter, end=' ')
            if i == AND: print("AND")
            elif i == OR: print("OR")
            elif i == XOR: print("XOR")
            elif i == NAND: print("NAND")
            elif i == NOR: print("NOR")
            elif i == XNOR: print("XNOR")
            counter += 1

def read_from_file(path):
    file_content = pd.read_csv(path)
    file_content.replace('TRUE', True, inplace = True)
    file_content.replace('FALSE', False, inplace = True)
    return file_content.values.tolist()

def generate_population(input_size):
    population = []
    for i in range(POPULATION_SIZE):
        ch = Chromosome()
        for j in range(input_size - 1):
            ch.gene.append(r.randrange(0,6))
        ch.fitness = get_fitness(ch.gene)
        population.append(ch)
    return population

def get_fitness(gene):
    fitness = 0
    for row in truth_table:
        value = row[0]
        k = 0
        while k < len(gene):
            if gene[k] == AND:
                value = value and row[k + 1]
            elif gene[k] == OR:
                value = value or row[k + 1]
            elif gene[k] == XOR:
                value = value != row[k + 1]
            elif gene[k] == NAND:
                value = not(value and row[k + 1])
            elif gene[k] == NOR:
                value = not(value or row[k + 1])
            elif gene[k] == XNOR:
                value = not(value != row[k + 1])
            k += 1
        if value == row[len(row) - 1]:
            fitness += 1
    return fitness

def reproduction(parent1, parent2):
    child1 = Chromosome()
    child2 = Chromosome()
    pos = r.randrange(0, number_of_inputs - 1)
    child1.gene = parent1.gene[:pos] + parent2.gene[pos:]
    child2.gene = parent2.gene[:pos] + parent1.gene[pos:]
    child1.fitness = get_fitness(child1.gene)
    child2.fitness = get_fitness(child2.gene)
    return child1, child2

def crossover(population):
    result = []
    pc = 0
    for chromosome in population:
        pc += chromosome.fitness
    pc = pc / POPULATION_SIZE 
    while len(population) > 1:
        i = r.randrange(0, len(population))
        ch1 = population.pop(i)
        j = r.randrange(0, len(population))
        ch2 = population.pop(j)
        possibility = r.randrange(1, 2**number_of_inputs)
        if possibility < pc:
            result.append(ch1)
            result.append(ch2)
        else:
            child1, child2 = reproduction(ch1, ch2)
            result.append(child1)
            result.append(child2)
    if len(population) == 1:
        result.append(population.pop())
    return result

def mutation(population):
    pm = MUTATION_RATE_LESS if counter < POPULATION_SIZE / 10 else MUTATION_RATE_MORE
    for chromosome in population:
        if chromosome.fitness == 2**number_of_inputs:
            return chromosome
        index = r.randrange(0, number_of_inputs - 1)
        possibility = r.uniform(0, 1)
        if possibility < pm:
            chromosome.gene[index] = r.randrange(0,6)
            chromosome.fitness = get_fitness(chromosome.gene)

def get_rand():
    index = 0
    rand = r.randrange(0, ((POPULATION_SIZE + 1) * POPULATION_SIZE) / 2)
    i = POPULATION_SIZE
    j = POPULATION_SIZE - 1
    while i <= rand:
        i += j
        j -= 1
        index += 1
    return index

def selection(population):
    population.sort(key=lambda x: x.fitness, reverse=True)
    i = 0
    result = []
    while i < POPULATION_SIZE:
        index = get_rand()
        result.append(population[index])
        i += 1
    population.clear()
    return result
    
if __name__ == "__main__":
    global number_of_inputs, truth_table, POPULATION_SIZE, MUTATION_RATE_LESS, MUTATION_RATE_MORE, counter
    truth_table = read_from_file(sys.argv[1])
    number_of_inputs = len(truth_table[0]) - 1
    POPULATION_SIZE = int(5**(number_of_inputs - 1) / 4000)
    MUTATION_RATE_LESS = 1 / POPULATION_SIZE
    MUTATION_RATE_MORE = 1 / (number_of_inputs - 1)

    tic = time.time()
    population = generate_population(number_of_inputs)
    counter = 0
    while True:
        population = selection(population)
        population = crossover(population)
        rv = mutation(population)
        if rv != None:
            rv.print()
            break
        counter += 1
    toc = time.time()
    print("Time: %f ms" % ((toc - tic) * 1000))