import pygad
import random
import numpy as np
import matplotlib.pyplot as plt

# ======================== PROBLEM PARAMETERS ========================
N = 100  # Number of available items (days)
restart_cost = 10000  # Cost to restart the plant after it being shut down
prod_per_day = 100  # Revenue from a running day (smallest possible time frame)

# List of electricity prices (randomized for testing)
random.seed(42)
prices = [random.randint(9, 200) for _ in range(N)]


# ======================== FITNESS FUNCTION ========================
def fitness_func(ga_instance, solution, solution_idx, return_revenue_curve=False):
    """Evaluates the total revenue while considering restart costs and electricity prices.
       If return_revenue_curve=True, also returns the cumulative revenue over time."""
    binary_solution = np.round(solution).astype(int)  # Ensure binary representation

    revenue = 0
    running = False  # Plant starts off
    revenue_over_time = []  # Track revenue per day

    for idx in range(N):
        if binary_solution[idx]:  # If the plant is running
            if not running:  # If restarting
                revenue -= restart_cost
                running = True
            revenue += prod_per_day  # Add revenue
            revenue -= prices[idx]  # Subtract electricity cost
        else:
            running = False  # The plant is off

        revenue_over_time.append(revenue)  # Store cumulative revenue

    return (revenue, revenue_over_time) if return_revenue_curve else revenue


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
    fitness_func=lambda ga, sol, idx: fitness_func(ga, sol, idx),  # Fitness function only returns revenue
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

# Compute revenue over time for best solution
_, revenue_over_time = fitness_func(ga_instance, binary_solution, solution_idx, return_revenue_curve=True)

# ======================== PLOTTING ========================
fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Plot 1: Electricity Prices + Running Periods
ax[0].plot(prices, label="Electricity Price ($)", color="blue", linestyle="dashed", alpha=0.7)
ax[0].fill_between(range(N), prices, where=binary_solution == 1, color="green", alpha=0.3, label="Plant Running")
ax[0].set_ylabel("Price ($)")
ax[0].set_title("Electricity Prices Over Time (Shaded = Running Periods)")
ax[0].legend()
ax[0].grid()

# Plot 2: Revenue Accumulation
ax[1].plot(revenue_over_time, label="Cumulative Revenue ($)", color="red", linewidth=2)
ax[1].set_xlabel("Day")
ax[1].set_ylabel("Revenue ($)")
ax[1].set_title("Revenue Over Time for Best Solution")
ax[1].legend()
ax[1].grid()

plt.tight_layout()
plt.show()

# Print solution and fitness
print("Best solution:")
print("[" + "".join("█" if binary_solution[idx] else " " for idx in range(N)) + "]")
print(f"Best solution fitness: {solution_fitness}")

# Compare with a full-time operation scenario
non_stop_fitness, _ = fitness_func(ga_instance, np.ones(N), solution_idx, return_revenue_curve=True)
print(f"Fitness of non-stop solution: {non_stop_fitness}")
