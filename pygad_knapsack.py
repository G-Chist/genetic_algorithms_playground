import pygad
import random
import numpy as np


# ======================== PROBLEM PARAMETERS ========================
N = 100  # Number of available items
W = 300  # Maximum weight capacity of the knapsack

# List of items, where each item is represented as a tuple (value, weight)
items = [(random.randint(1, 10), random.randint(1, 10)) for _ in range(N)]


# ======================== FITNESS FUNCTION ========================
def fitness_func(ga_instance, solution, solution_idx):
    total_value = sum(items[i][0] for i in range(N) if solution[i] == 1)  # Use strict binary values
    total_weight = sum(items[i][1] for i in range(N) if solution[i] == 1)

    return total_value if total_weight <= W else 0  # Penalize overweight solutions


# ======================== WEIGHT FUNCTION ========================
def weight(solution):
    return sum(items[i][1] for i in range(N) if solution[i] == 1)


# ======================== BINARY CONSTRAINT FIXES ========================
def binary_mutation(offspring, ga_instance):
    """ Custom mutation function that flips 0s to 1s and vice versa. """
    mutation_indices = np.random.choice(len(offspring), size=int(len(offspring) * 0.3), replace=False)
    for i in mutation_indices:
        offspring[i] = 1 - offspring[i]  # Flip the bit
    return offspring


# ======================== GA PARAMETERS ========================
num_generations = 1000
num_parents_mating = 4
sol_per_pop = 20
num_genes = N

# Initialize population with strictly binary values (0s and 1s)
initial_population = np.random.choice([0, 1], size=(sol_per_pop, num_genes))

ga_instance = pygad.GA(
    num_generations=num_generations,
    num_parents_mating=num_parents_mating,
    fitness_func=fitness_func,
    sol_per_pop=sol_per_pop,
    num_genes=num_genes,
    parent_selection_type="sss",
    keep_parents=2,
    crossover_type="single_point",
    mutation_type=binary_mutation,  # Use custom mutation function
    mutation_percent_genes=30,
    initial_population=initial_population  # Enforce binary initialization
)

# ======================== RUN GA ========================
ga_instance.run()

# ======================== OUTPUT RESULTS ========================
solution, solution_fitness, solution_idx = ga_instance.best_solution()

print("Best solution:")
print(solution.tolist())  # Output strictly 0/1 values
print(f"Best solution fitness: {solution_fitness}")
print(f"Total weight of items picked: {weight(solution)} / {W}")
