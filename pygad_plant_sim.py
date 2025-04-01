import pygad
import random
import numpy as np
import matplotlib.pyplot as plt
import math
import os

# ======================== PROBLEM PARAMETERS ========================
N = 2000  # Number of available items (days)
restart_cost = 500  # Cost to restart the plant after it being shut down
prod_per_day = 100  # Revenue from a running day (smallest possible time frame)
switch_constant = 10  # If a solution has frequent switches, we will not prioritize it
switch_fitness_decrement = 1000  # Decrease a solution's fitness by this if it has frequent switches

# List of electricity prices (randomized for testing)
random.seed(1)
# Fuzzy sine wave
prices = [100 + random.uniform(30, 50)*math.sin((i/80)*random.uniform(0.6, 1.2)) + random.randint(-5, 5) for i in range(N)]


# ======================== FITNESS FUNCTION ========================
def fitness_func(ga_instance, solution, solution_idx, return_revenue_curve=False):
    """Evaluates the total revenue while considering restart costs and electricity prices.
       If return_revenue_curve=True, also returns the cumulative revenue over time."""
    binary_solution = np.round(solution).astype(int)  # Ensure binary representation

    revenue = 0
    fitness = 0
    running = False  # Plant starts off
    revenue_over_time = []  # Track revenue per day
    last_switch = 0  # Track state switching frequency

    for idx in range(N):
        if binary_solution[idx]:  # If the plant is running
            if not running:  # If restarting
                revenue -= restart_cost
                running = True
                if last_switch < switch_constant:  # If the solution switches the state too abruptly, decrease fitness
                    fitness -= switch_fitness_decrement
            revenue += prod_per_day  # Add revenue
            revenue -= prices[idx]  # Subtract electricity cost
            last_switch += 1
        else:
            running = False  # The plant is off
            last_switch = 0

        revenue_over_time.append(revenue)  # Store cumulative revenue

    fitness += revenue

    return (revenue, revenue_over_time) if return_revenue_curve else revenue


# ======================== CUSTOM MUTATION FUNCTION ========================
def binary_mutation(offspring, ga_instance):
    """Bit-flip mutation (flips bits in each offspring)."""
    mutation_indices = np.random.choice(len(offspring), size=int(len(offspring) * 0.2), replace=False)
    for i in mutation_indices:
        offspring[i] = 1 - offspring[i]  # Flip bit (0 ↔ 1)
    return offspring


# ======================== GA PARAMETERS ========================
num_generations = 500
num_parents_mating = 16
sol_per_pop = 50
num_genes = N

# Strictly binary initial population
initial_population = [np.ones(N) for _ in range(sol_per_pop)]  # Initialize all ones

ga_instance = pygad.GA(
    num_generations=num_generations,
    num_parents_mating=num_parents_mating,
    fitness_func=lambda ga, sol, idx: fitness_func(ga, sol, idx),  # Fitness function only returns revenue
    sol_per_pop=sol_per_pop,
    num_genes=num_genes,
    parent_selection_type="random",
    keep_parents=4,
    crossover_type="single_point",
    mutation_type=binary_mutation,  # Use custom mutation
    initial_population=initial_population
)

# ======================== RUN GA ========================
ga_instance.run()  # Start the genetic algorithm

# ======================== SECONDARY TRAINING WITH STEADY-STATE SELECTION ========================
solution, solution_fitness, solution_idx = ga_instance.best_solution()

ga_instance = pygad.GA(
    num_generations=num_generations//2,
    num_parents_mating=num_parents_mating,
    fitness_func=lambda ga, sol, idx: fitness_func(ga, sol, idx),  # Fitness function only returns revenue
    sol_per_pop=sol_per_pop,
    num_genes=num_genes,
    parent_selection_type="sss",  # Steady-State Selection
    keep_parents=4,
    crossover_type="single_point",
    mutation_type=binary_mutation,  # Use custom mutation
    initial_population=[solution for _ in range(sol_per_pop)]
)

# ======================== OUTPUT RESULTS ========================
solution, solution_fitness, solution_idx = ga_instance.best_solution()
binary_solution = np.round(solution).astype(int)  # Convert to strictly binary values

# Compute revenue over time for best solution
_, revenue_over_time = fitness_func(ga_instance, binary_solution, solution_idx, return_revenue_curve=True)

# Print solution and fitness
print("Best solution:")
print("[" + "".join("█" if binary_solution[idx] else " " for idx in range(N)) + "]")
print(f"Best solution fitness: {solution_fitness}")

# Compare with a full-time operation scenario
non_stop_fitness, _ = fitness_func(ga_instance, np.ones(N), solution_idx, return_revenue_curve=True)
print(f"Fitness of non-stop solution: {non_stop_fitness}")

# ======================== PLOTTING ========================
fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Plot 1: Electricity Prices + Running Periods
ax[0].plot(prices, label="Electricity Price ($)", color="blue", linestyle="dashed", alpha=0.7)
ax[0].plot([prod_per_day for _ in range(N)], label="Daily revenue (ignoring electricity prices) ($)", color="orange", alpha=0.7)
ax[0].fill_between(range(N), prices, where=binary_solution == 1, color="green", alpha=0.3, label="Plant Running")
ax[0].set_ylabel("Price ($)")
ax[0].set_title("Electricity Prices Over Time (Shaded = Running Periods)")
ax[0].legend()
ax[0].grid()

# Plot 2: Revenue Accumulation
ax[1].plot(revenue_over_time, label="Cumulative Revenue (Best Solution)", color="red", linewidth=2)
# Compute non-stop solution revenue over time
non_stop_solution = np.ones(N)  # Plant runs all the time
_, non_stop_revenue_over_time = fitness_func(ga_instance, non_stop_solution, solution_idx, return_revenue_curve=True)
ax[1].plot(non_stop_revenue_over_time, label="Cumulative Revenue (Non-Stop Solution)", color="blue", linestyle="--", linewidth=2)
ax[1].set_xlabel("Day")
ax[1].set_ylabel("Revenue ($)")
ax[1].set_title("Revenue Over Time for Best Solution vs Non-Stop Solution")
ax[1].legend()
ax[1].grid()

plt.tight_layout()
plt.show()

# Create directory if it doesn't exist
output_dir = "plant_sim"
os.makedirs(output_dir, exist_ok=True)

# Save the figure
output_path = os.path.join(output_dir, "plant_simulation.png")
fig.savefig(output_path, dpi=300)
print(f"Plot saved to {output_path}")
