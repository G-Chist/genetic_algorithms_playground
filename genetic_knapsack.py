import random

# ======================== PROBLEM PARAMETERS ========================
N = 100  # Number of available items
W = 300  # Maximum weight capacity of the knapsack

# List of items, where each item is represented as a tuple (value, weight)
items = [
    (random.randint(1, 10), random.randint(1, 10)) for i in range(N)
]

# ======================== GENETIC ALGORITHM PARAMETERS ========================
POP_SIZE = 100  # Number of solutions (chromosomes) per generation
MUTATION_RATE = 0.1  # Probability of mutation occurring in an offspring
GENERATIONS = 500  # Total number of generations to evolve

# ======================== FUNCTION DEFINITIONS ========================


# Function to generate a random binary solution (chromosome)
# Each gene in the chromosome represents whether an item is included (1) or not (0)
def random_solution():
    return [random.randint(0, 1) for _ in range(N)]  # Randomly assign 0 or 1 to each item


# Fitness function to evaluate the quality of a solution
# It sums up the values of selected items if the total weight is within capacity
# If the weight exceeds the limit, the solution is considered invalid (fitness = 0)
def fitness(solution):
    total_value = sum(items[i][0] for i in range(N) if solution[i] == 1)  # Calculate total value
    total_weight = sum(items[i][1] for i in range(N) if solution[i] == 1)  # Calculate total weight
    return total_value if total_weight <= W else 0  # Return value if within weight limit, otherwise 0


# Selection function using tournament selection
# Randomly selects 3 solutions from the population and returns the best one (highest fitness)
def select(population):
    return max(random.sample(population, 3), key=fitness)  # Pick 3 random solutions and return the best


# Crossover function using single-point crossover
# It combines genetic material from two parents to create a new solution (offspring)
def crossover(parent1, parent2):
    point = random.randint(1, N - 1)  # Select a random crossover point (not at the edges)
    return parent1[:point] + parent2[point:]  # Combine genes from both parents


# Mutation function that randomly flips a gene with a small probability
def mutate(solution):
    if random.random() < MUTATION_RATE:  # Apply mutation with the given probability
        index = random.randint(0, N - 1)  # Select a random gene (item)
        solution[index] = 1 - solution[index]  # Flip the bit (0 -> 1, or 1 -> 0)
    return solution  # Return the mutated solution


# ======================== MAIN GENETIC ALGORITHM ========================
def genetic_algorithm():
    # Step 1: Initialize the population with random solutions
    population = [random_solution() for _ in range(POP_SIZE)]

    # Step 2: Iterate through generations to evolve better solutions
    for _ in range(GENERATIONS):
        new_population = []  # Create a new population for the next generation

        # Step 3: Generate new offspring by selecting parents and applying crossover/mutation
        for _ in range(POP_SIZE // 2):  # Each iteration produces two new offspring
            parent1, parent2 = select(population), select(population)  # Select two parents
            child1, child2 = crossover(parent1, parent2), crossover(parent2, parent1)  # Perform crossover
            new_population.extend([mutate(child1), mutate(child2)])  # Apply mutation and add to new population

        # Step 4: Replace the old population with the new one
        population = new_population

    # Step 5: Identify the best solution in the final population
    best_solution = max(population, key=fitness)
    return best_solution, fitness(best_solution)  # Return the best chromosome and its fitness value


# ======================== RUN THE ALGORITHM ========================
best_solution, best_value = genetic_algorithm()  # Execute the genetic algorithm

# ======================== DISPLAY THE RESULTS ========================
print("Best Solution:", best_solution)  # Print the best chromosome (binary representation)
print("Best Value Achieved:", best_value)  # Print the maximum value obtained within weight constraints
print("Items selected: ", best_solution.count(1), "/", str(N))  # Print out the selected item count

counter = 0
for value, weight in items:
    counter += 1
    if best_solution[counter-1] == 1:
        print(f"Item {counter}: value = {value}, weight = {weight}")  # Print out selected items
