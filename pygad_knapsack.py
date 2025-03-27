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
    mutation_type="swap",
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
