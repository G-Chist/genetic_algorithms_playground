import pygad
import random
import numpy as np

# ======================== PROBLEM PARAMETERS ========================
N = 100  # Number of available items (days)
restart_cost = 10000  # Cost to restart the plant after it being shut down
prod_per_day = 100  # Revenue from a running day (smallest possible time frame)

# List of electricity prices (randomized for testing)
random.seed(42)
prices = [random.randint(9, 200) for _ in range(N)]


# ======================== FITNESS FUNCTION ========================
def fitness_func(ga_instance, solution, solution_idx):
    """
    Evaluates the total revenue while considering restart costs and electricity prices.
    """
    binary_solution = np.round(solution).astype(int)  # Ensure binary representation

    revenue = 0
    running = False  # Plant starts off

    for idx in range(N):
        if binary_solution[idx]:  # If the plant is running
            if not running:  # If restarting
                revenue -= restart_cost
                running = True
            revenue += prod_per_day  # Add revenue
            revenue -= prices[idx]   # Subtract electricity cost
        else:
            running = False  # The plant is off

    return revenue


# ======================== CUSTOM MUTATION FUNCTION ========================
def binary_mutation(offspring, ga_instance):
    """Bit-flip mutation (flips 10% of bits in each offspring)."""
    mutation_indices = np.random.choice(len(offspring), size=int(len(offspring) * 0.1), replace=False)
    for i in mutation_indices:
        offspring[i] = 1 - offspring[i]  # Flip bit (0 ↔ 1)
    return offspring


# ======================== GA PARAMETERS ========================
num_generations = 1000
num_parents_mating = 16
sol_per_pop = 100
num_genes = N

# Strictly binary initial population
initial_population = np.random.choice([0, 1], size=(sol_per_pop, num_genes)).astype(int)

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

# Print visual representation of the best solution
print("Best solution:")
print("[" + "".join("█" if binary_solution[idx] else " " for idx in range(N)) + "]")
print(f"Best solution fitness: {solution_fitness}")

# Compare with a full-time operation scenario
non_stop_fitness = fitness_func(ga_instance, np.ones(N), solution_idx)
print(f"Fitness of non-stop solution: {non_stop_fitness}")
