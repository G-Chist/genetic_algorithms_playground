import pygad
import random

# ======================== PROBLEM PARAMETERS ========================
N = 100  # Number of available items
W = 300  # Maximum weight capacity of the knapsack

# List of items, where each item is represented as a tuple (value, weight)
items = [
    (random.randint(1, 10), random.randint(1, 10)) for i in range(N)
]

# Set parameters for the genetic algorithm
num_generations = 1000  # The number of generations the GA will run
num_parents_mating = 4  # The number of parents selected for mating
sol_per_pop = 20  # Number of solutions in each population
num_genes = N  # Number of genes
init_range_low = 0  # The lower limit for each gene
init_range_high = 1  # The upper limit for each gene

