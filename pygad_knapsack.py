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
    """
    The fitness function calculates the total value of selected items
    while ensuring that the total weight does not exceed the maximum allowed weight (W).
    """
    binary_solution = np.round(solution).astype(int)  # Ensure binary representation

    total_value = sum(items[i][0] for i in range(N) if binary_solution[i])  # Sum values
    total_weight = sum(items[i][1] for i in range(N) if binary_solution[i])  # Sum weights

    return total_value if total_weight <= W else 0  # Penalize overweight solutions


# ======================== WEIGHT FUNCTION ========================
def weight(solution):
    """Computes the total weight of the selected items."""
    binary_solution = np.round(solution).astype(int)
    return sum(items[i][1] for i in range(N) if binary_solution[i])


# ======================== GA PARAMETERS ========================
num_generations = 500
num_parents_mating = 4
sol_per_pop = 100
num_genes = N

# Enforce strictly binary initial population
initial_population = np.random.choice([0, 1], size=(sol_per_pop, num_genes)).astype(int)


# Custom mutation function (bit-flip mutation)
def binary_mutation(offspring, ga_instance):
    mutation_indices = np.random.choice(len(offspring), size=int(len(offspring) * 0.1), replace=False)
    for i in mutation_indices:
        offspring[i] = 1 - offspring[i]  # Flip bit
    return offspring


ga_instance = pygad.GA(
    num_generations=num_generations,
    num_parents_mating=num_parents_mating,
    fitness_func=fitness_func,
    sol_per_pop=sol_per_pop,
    num_genes=num_genes,
    parent_selection_type="sss",
    keep_parents=2,
    crossover_type="single_point",
    mutation_type=binary_mutation,  # Use custom mutation
    initial_population=initial_population
)

# ======================== RUN GA ========================
ga_instance.run()  # Start the genetic algorithm

# ======================== OUTPUT RESULTS ========================
solution, solution_fitness, solution_idx = ga_instance.best_solution()
binary_solution = np.round(solution).astype(int)  # Convert to strictly binary values

print("Best solution:")
print("[", end="")
for idx in range(N):
    if round(solution[idx]) == 1:
        print("█", end="")
    else:
        print(" ", end="")
print("]")
print(f"Best solution fitness: {solution_fitness}")
print(f"Total weight of items picked: {weight(solution)} / {W}")
