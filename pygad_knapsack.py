import pygad
import random


# Function to turn value into binary
def clamp(value):
    if value > 0.5:
        return 1
    return 0


# ======================== PROBLEM PARAMETERS ========================
N = 100  # Number of available items
W = 300  # Maximum weight capacity of the knapsack


def fitness_func(ga_instance, solution, solution_idx):
    total_value = sum(items[i][0] for i in range(N) if solution[i] > 0.5)  # Calculate total value
    total_weight = sum(items[i][1] for i in range(N) if solution[i] > 0.5)  # Calculate total weight
    return total_value if total_weight <= W else 0  # Return value if within weight limit, otherwise 0


def weight(solution):
    total_weight = sum(items[i][1] for i in range(N) if solution[i] > 0.5)  # Calculate total weight
    return total_weight


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

# Set the types of parent selection, crossover, and mutation methods
parent_selection_type = "sss"  # "sss" stands for Steady State Selection (a parent selection method)
"""In every generation few chromosomes are selected (good - with high fitness) for creating a new offspring.
Then some (bad - with low fitness) chromosomes are removed and the new offspring is placed in their place.
The rest of population survives to new generation.
"""
keep_parents = 2  # Number of parents to keep from one generation to the next
crossover_type = "single_point"  # Single-point crossover method is used to combine parent solutions
mutation_type = "random"  # Random mutation method will be used to introduce variation
mutation_percent_genes = 30  # Percentage of genes that will undergo mutation in each generation

# Initialize the genetic algorithm instance with all the parameters
ga_instance = pygad.GA(
    num_generations=num_generations,  # Set number of generations
    num_parents_mating=num_parents_mating,  # Set number of parents mating
    fitness_func=fitness_func,  # Assign the fitness function
    sol_per_pop=sol_per_pop,  # Set the number of solutions per population
    num_genes=num_genes,  # Set the number of genes (polynomial coefficients)
    init_range_low=init_range_low,  # Set the lower limit for gene initialization
    init_range_high=init_range_high,  # Set the upper limit for gene initialization
    parent_selection_type=parent_selection_type,  # Parent selection method
    keep_parents=keep_parents,  # Number of parents to keep in the next generation
    crossover_type=crossover_type,  # Crossover method
    mutation_type=mutation_type,  # Mutation method
    mutation_percent_genes=mutation_percent_genes  # Percentage of genes to mutate
)

# Run the genetic algorithm
ga_instance.run()  # The GA runs for the specified number of generations

# Get the best solution found by the GA after all generations
solution, solution_fitness, solution_idx = ga_instance.best_solution()  # Retrieve the best solution

print("Best solution:")
print([clamp(i) for i in solution])  # Convert solution to array of bits
print(f"Best solution fitness: {solution_fitness}")

print(f"Total weight of items picked: {weight(solution)} / {W}")
