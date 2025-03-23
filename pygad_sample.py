import pygad
import numpy as np
import matplotlib.pyplot as plt


# The sine function we want to match
def target_function(x):
    return np.sin(x)


# Polynomial function of the form ax^3 + bx^2 + cx + d
def polynomial_function(x, coefficients):
    a, b, c, d = coefficients
    return a * (x ** 3) + b * (x ** 2) + c * x + d


# Fitness function to evaluate how well the polynomial matches sin(x)
def fitness_func(ga_instance, solution, solution_idx):
    # We will evaluate the fitness over the range of x from 0 to 2*pi
    x_values = np.linspace(-np.pi, np.pi, 100)  # Generate 100 values of x from -pi to pi
    target_values = target_function(x_values)  # Actual sin(x) values
    predicted_values = polynomial_function(x_values, solution)  # Polynomial values

    # Compute the squared error between the polynomial and the target function (sin(x))
    error = np.sum((predicted_values - target_values) ** 2)  # Squared error is commonly used for regression tasks
    fitness = 1.0 / (1.0 + error)  # We return the inverse of error, so the fitness is higher when error is smaller
    return fitness


# Genetic algorithm parameters
num_generations = 1000
num_parents_mating = 4
sol_per_pop = 8
num_genes = 4  # a, b, c, d are the 4 coefficients of the polynomial
init_range_low = -5  # Coefficients can range from -5 to 5
init_range_high = 5

# Define the parent selection, crossover, and mutation methods
parent_selection_type = "sss"
keep_parents = 1
crossover_type = "single_point"
mutation_type = "random"
mutation_percent_genes = 10

# Initialize the genetic algorithm instance
ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_func,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       init_range_low=init_range_low,
                       init_range_high=init_range_high,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes)

# Run the genetic algorithm
ga_instance.run()

# Get the best solution found by the GA
solution, solution_fitness, solution_idx = ga_instance.best_solution()

# Print out the best solution (the coefficients of the polynomial)
print("Best polynomial coefficients: a = {0}, b = {1}, c = {2}, d = {3}".format(solution[0], solution[1], solution[2],
                                                                                solution[3]))
print("Fitness value of the best solution = {0}".format(solution_fitness))

# Test the polynomial with the best coefficients and compare to sin(x)
x_values = np.linspace(-2* np.pi, 2 * np.pi, 100)
predicted_values = polynomial_function(x_values, solution)
target_values = target_function(x_values)

# Plot the results
plt.xlim(-5, 5)
plt.ylim(-1.5, 1.5)
plt.plot(x_values, target_values, label='sin(x)', color='blue')
plt.plot(x_values, predicted_values, label='Polynomial', color='red', linestyle='dashed')
plt.legend()
plt.title('Polynomial vs. sin(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
