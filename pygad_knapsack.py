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

    If the total weight exceeds W, the solution is considered invalid and gets a fitness score of 0.
    """
    total_value = sum(items[i][0] for i in range(N) if round(solution[i]) == 1)  # Sum values of selected items
    total_weight = sum(items[i][1] for i in range(N) if round(solution[i]) == 1)  # Sum weights of selected items

    return total_value if total_weight <= W else 0  # Penalize overweight solutions


# ======================== WEIGHT FUNCTION ========================
def weight(solution):
    """
    Computes the total weight of the selected items in the solution.
    This function helps validate the feasibility of the best solution.
    """
    return sum(items[i][1] for i in range(N) if round(solution[i]) == 1)


# ======================== CUSTOM BINARY MUTATION FUNCTION ========================
def binary_mutation(offspring, ga_instance):
    """
    Custom mutation function that ensures the solution remains binary (0s and 1s).

    Mutation works by randomly selecting some genes (items) and flipping their values:
    - If a gene is 0, it becomes 1 (item is added to the knapsack).
    - If a gene is 1, it becomes 0 (item is removed from the knapsack).

    The number of genes selected for mutation is determined by `mutation_percent_genes`.

    Parameters:
    - offspring: The current solution being mutated.
    - ga_instance: The GA instance (not used directly here).

    Returns:
    - A mutated version of the offspring with flipped bits.
    """

    for i in range(len(offspring)):  # Loop over each offspring
        mutation_indices = np.random.choice(len(offspring[i]), size=int(len(offspring[i]) * 0.1), replace=False)
        for idx in mutation_indices:
            offspring[i, idx] = 1 - offspring[i, idx]  # Flip bit (0 -> 1, 1 -> 0)
    return offspring


# ======================== GA PARAMETERS ========================
num_generations = 500
num_parents_mating = 4
sol_per_pop = 100
num_genes = N

# Initialize population with strictly binary values (0s and 1s)
initial_population = np.random.choice([0, 1], size=(sol_per_pop, num_genes))

ga_instance = pygad.GA(
    num_generations=num_generations,  # Number of generations the GA will evolve
    num_parents_mating=num_parents_mating,  # Number of parents selected for reproduction
    fitness_func=fitness_func,  # The function used to evaluate solutions
    sol_per_pop=sol_per_pop,  # Number of solutions in each generation
    num_genes=num_genes,  # Number of genes (equal to number of items)
    parent_selection_type="sss",  # Steady-State Selection for choosing parents
    keep_parents=2,  # Number of parents carried to the next generation
    crossover_type="single_point",  # Single-point crossover for genetic mixing
    mutation_type=binary_mutation,  # Use our custom binary mutation function
    mutation_percent_genes=10,  # Mutate 10% of the genes in each offspring
    initial_population=initial_population  # Ensure population starts as binary
)

# ======================== RUN GA ========================
ga_instance.run()  # Start the genetic algorithm

# ======================== OUTPUT RESULTS ========================
solution, solution_fitness, solution_idx = ga_instance.best_solution()

print("Best solution:")
print(solution.tolist())  # Convert NumPy array to a Python list for readability
print(f"Best solution fitness: {solution_fitness}")
print(f"Total weight of items picked: {weight(solution)} / {W}")
