# Import necessary libraries
import pygad  # PyGAD is used for genetic algorithm functionality
import numpy as np  # Numpy is used for numerical operations and array manipulations
import matplotlib.pyplot as plt  # Matplotlib is used for plotting results


# Define the target function (sin(x)) we want to approximate
def target_function(x):
    return np.sin(x)  # The target function is sin(x)


# Define the polynomial function (ax^3 + bx^2 + cx + d)
def polynomial_function(x, coefficients):
    # Extract polynomial coefficients
    a, b, c, d = coefficients
    # Return the value of the polynomial for given x
    return a * (x ** 3) + b * (x ** 2) + c * x + d


# Fitness function evaluates how well the polynomial approximates sin(x)
def fitness_func(ga_instance, solution, solution_idx):
    # Generate a range of x values from -pi to pi
    x_values = np.linspace(-np.pi, np.pi, 100)  # Generate points
    target_values = target_function(x_values)  # Get the actual sin(x) values
    predicted_values = polynomial_function(x_values, solution)  # Get the predicted values from the polynomial

    # Compute the squared error between predicted and target sin(x) values
    error = np.sum((predicted_values - target_values) ** 2)  # Squared error is used to quantify the difference
    # Fitness is the inverse of error: lower error = better fitness
    fitness = 1.0 / (1.0 + error)  # Higher fitness corresponds to a better solution
    return fitness  # Return fitness value for the solution


# Set parameters for the genetic algorithm
num_generations = 1000  # The number of generations the GA will run
num_parents_mating = 4  # The number of parents selected for mating
sol_per_pop = 20  # Number of solutions in each population
num_genes = 4  # Number of genes (coefficients) for the polynomial
init_range_low = -5  # The lower bound for polynomial coefficients
init_range_high = 5  # The upper bound for polynomial coefficients

# Set the types of parent selection, crossover, and mutation methods
parent_selection_type = "sss"  # "sss" stands for Steady State Selection (a parent selection method)
"""In every generation few chromosomes are selected (good - with high fitness) for creating a new offspring.
Then some (bad - with low fitness) chromosomes are removed and the new offspring is placed in their place.
The rest of population survives to new generation.
"""
keep_parents = 2  # Number of parents to keep from one generation to the next
crossover_type = "single_point"  # Single-point crossover method is used to combine parent solutions
mutation_type = "random"  # Random mutation method will be used to introduce variation
mutation_percent_genes = 10  # Percentage of genes that will undergo mutation in each generation

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

# Print the best solution's polynomial coefficients and fitness value
print("Best polynomial coefficients: a = {0}, b = {1}, c = {2}, d = {3}".format(
    solution[0], solution[1], solution[2], solution[3]))  # Print coefficients for the polynomial
print("Fitness value of the best solution = {0}".format(solution_fitness))  # Print fitness value

# Generate x values for plotting the polynomial and sin(x)
x_values = np.linspace(-3 * np.pi, 3 * np.pi, 100)  # Generate values of x
# Get the predicted polynomial values for these x values using the best solution
predicted_values = polynomial_function(x_values, solution)
# Get the target sin(x) values for the same x values
target_values = target_function(x_values)

# Plot the actual sin(x) values (target function) and the predicted polynomial values
fig, ax = plt.subplots()  # Create a figure and axes object

# Plot sin(x) in blue
ax.plot(x_values, target_values, label='sin(x)', color='blue')

# Plot the polynomial in red with a dashed line
ax.plot(x_values, predicted_values, label='Polynomial', color='red', linestyle='dashed')

ax.set_xlim(-10, 10)  # Limit x-axis
ax.set_ylim(-10, 10)  # Limit y-axis

# Add legend to the plot
ax.legend()

# Add a title and labels to the plot
ax.set_title('Polynomial vs. sin(x)')
ax.set_xlabel('x')
ax.set_ylabel('y')

# Enforce equal scaling of both axes
# ax.axis('equal')

# Add axis arrows using ax.arrow
ax.arrow(-20, 0, 40, 0, head_width=0.5, head_length=1, fc='black', ec='black')
ax.arrow(0, -20, 0, 40, head_width=0.5, head_length=1, fc='black', ec='black')

# Show the plot
plt.show()
