# Import necessary libraries
import random  # For generating random values
import math  # For mathematical operations, specifically sine function
import numpy as np  # For numerical operations like creating ranges and handling arrays
import matplotlib.pyplot as plt  # For plotting graphs
import matplotlib.animation as animation  # For creating animated visualizations


# Define the polynomial function (cubic equation)
def polynomial(a, b, c, d, x):
    """
    This function defines the polynomial of the form: a*x^3 + b*x^2 + c*x + d
    Parameters:
    a, b, c, d: coefficients of the cubic equation
    x: input variable
    Returns:
    The value of the polynomial at x
    """
    return a * (x ** 3) + b * (x * x) + c * x + d


# Define the function that we want to approximate (sin(x) in this case)
def func_to_approximate(x):
    """
    This is the reference function we want to approximate using a cubic polynomial.
    In this case, we are using the sine function.
    Parameters:
    x: input variable
    Returns:
    The sine of x
    """
    return math.sin(x)


# Define the fitness function for genetic algorithm
def fitness_function(a, b, c, d, start=-2, end=2, step=0.05):
    """
    The fitness function evaluates how well a given polynomial approximates the sine function.
    It calculates the accumulated error between the polynomial and sine function over a range of x-values.

    Parameters:
    a, b, c, d: coefficients of the polynomial
    start, end: the range of x values to evaluate the error over
    step: step size between consecutive x values

    Returns:
    A fitness score, which is the inverse of the accumulated error (higher is better)
    """
    accumulated_error = 0
    # Loop through x values in the given range with the specified step
    for x in np.arange(start, end, step):
        # Add the absolute difference between the polynomial and the sine function to the error
        accumulated_error += abs(polynomial(a, b, c, d, x) - func_to_approximate(x))
    # Return the inverse of the error as the fitness score (higher score is better)
    return 1 / abs(accumulated_error)


# Function to generate a random individual (a random set of polynomial coefficients)
def generate_individual():
    """
    Generates a random individual with random coefficients for the cubic polynomial.

    Returns:
    A tuple with four random values representing the coefficients a, b, c, and d
    """
    return random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-0.1, 0.1)


# Function to generate an initial population of random individuals
def generate_population(size):
    """
    Generates an initial population of individuals (polynomials).

    Parameters:
    size: The number of individuals in the population

    Returns:
    A list of individuals (tuples of coefficients)
    """
    return [generate_individual() for _ in range(size)]


# Tournament selection function to choose parents for crossover
def tournament_selection(population, fitness_scores, k=2):
    """
    Selects a parent using tournament selection.
    The best individual from a randomly selected subset of size `k` is chosen as the parent.

    Parameters:
    population: List of individuals in the current population
    fitness_scores: List of fitness scores corresponding to the individuals
    k: Size of the tournament (default is 2)

    Returns:
    The best individual chosen as the parent
    """
    # Randomly sample 'k' individuals along with their fitness scores
    selected = random.sample(list(zip(population, fitness_scores)), k)
    # Return the individual with the highest fitness score
    return max(selected, key=lambda x: x[1])[0]


# Function to perform crossover between two parents to produce two children
def crossover(parent1, parent2):
    """
    Perform a one-point crossover between two parents to generate two children.

    Parameters:
    parent1, parent2: The two parent individuals (tuples of coefficients)

    Returns:
    Two child individuals, each a combination of parent1 and parent2
    """
    crossover_point = random.randint(1, 3)  # Randomly choose a crossover point between 1 and 3
    child1 = parent1[:crossover_point] + parent2[crossover_point:]  # Combine parents to form child1
    child2 = parent2[:crossover_point] + parent1[crossover_point:]  # Combine parents to form child2
    return child1, child2


# Function to apply mutation to an individual (a set of polynomial coefficients)
def mutate(individual, mutation_rate=0.15):
    """
    Apply mutation to an individual. Mutation randomly adjusts one of the coefficients.

    Parameters:
    individual: The individual (a tuple of coefficients)
    mutation_rate: The probability that a mutation will occur (default 0.15)

    Returns:
    The mutated individual (if mutation occurs) or the original individual (if no mutation occurs)
    """
    if random.random() < mutation_rate:
        index = random.randint(0, 3)  # Randomly choose which coefficient to mutate (a, b, c, or d)
        mutated = list(individual)  # Convert the individual to a list to modify it
        mutated[index] *= random.uniform(0.9, 1.1)  # Adjust the chosen coefficient by a random factor
        return tuple(mutated)  # Return the mutated individual
    return individual  # If no mutation occurs, return the original individual


# Pre-generate the evolution of polynomials over generations (genetic algorithm loop)
def generate_evolution(population_size, max_generations, step_frequency=20):
    """
    Run the genetic algorithm to evolve the population of polynomials towards better approximations of sin(x).

    Parameters:
    population_size: The number of individuals in the population
    max_generations: The number of generations to evolve the population
    step_frequency: How often to store the best solution for animation purposes

    Returns:
    A list of the best individuals at each step of evolution
    """
    population = generate_population(population_size)  # Initialize the population
    evolution = []  # List to store the best individual at each step

    # Loop through each generation
    for generation in range(max_generations):
        # Evaluate the fitness of all individuals in the population
        fitness_scores = [fitness_function(*ind) for ind in population]
        best_individual = population[fitness_scores.index(max(fitness_scores))]  # Get the best individual

        # Store the best individual every `step_frequency` generations
        if generation % step_frequency == 0:
            evolution.append(best_individual)

        # Generate the next generation
        next_generation = []  # List to store the next generation of individuals
        while len(next_generation) < population_size:
            # Select two parents using tournament selection
            parent1 = tournament_selection(population, fitness_scores)
            parent2 = tournament_selection(population, fitness_scores)
            # Perform crossover to create two children
            child1, child2 = crossover(parent1, parent2)
            # Mutate the children and add them to the next generation
            next_generation.append(mutate(child1))
            if len(next_generation) < population_size:
                next_generation.append(mutate(child2))

        # Update the population for the next generation
        population = next_generation

    return evolution  # Return the list of best individuals over the generations


# Run the genetic algorithm to generate the evolution of polynomials
population_size = 50  # Set population size
max_generations = 1000  # Set the number of generations to run the algorithm
evolution = generate_evolution(population_size, max_generations, step_frequency=20)

# Set up the figure for plotting the animation
fig, ax = plt.subplots()  # Create a figure and axis for plotting
x_values = np.linspace(-5, 5, 500)  # Create an array of x values from -5 to 5
y_sin = np.sin(x_values)  # Compute the reference sine function values
line, = ax.plot(x_values, np.zeros_like(x_values), label="Evolving Polynomial", color="red")  # Initialize the plot

# Configure the plot appearance
ax.plot(x_values, y_sin, label="sin(x)", color="blue")  # Plot the reference sine function
ax.set_xlim(-5, 5)  # Set x-axis limits
ax.set_ylim(-1.5, 1.5)  # Set y-axis limits
ax.axhline(0, color='black', linewidth=0.5)  # Add horizontal axis line
ax.axvline(0, color='black', linewidth=0.5)  # Add vertical axis line
ax.grid(True, linestyle='--', alpha=0.6)  # Enable grid with dashed lines
ax.legend()  # Show the legend
ax.set_title("Evolution of Polynomial Approximation of sin(x)")  # Set the plot title


# Function to update the plot during animation
def update(frame):
    """
    Update the plot for each frame of the animation.

    Parameters:
    frame: The current frame index in the animation
    Returns:
    The updated line object with the new polynomial curve
    """
    best_individual = evolution[frame]  # Get the best individual for the current frame
    y_poly = best_individual[0] * x_values ** 3 + best_individual[1] * x_values ** 2 + best_individual[2] * x_values + \
             best_individual[3]  # Calculate the polynomial values for the x values
    line.set_ydata(y_poly)  # Update the y-data of the plot with the new polynomial values
    return line,  # Return the updated line object


# Create animation with a time step for each update
time_step = 50  # Control the speed of the animation by adjusting the time step
ani = animation.FuncAnimation(fig, update, frames=len(evolution), interval=time_step,
                              repeat=False)  # Create the animation

# Save the animation as a GIF using ImageMagick
ani.save('polynomial_approximation.gif', writer='imagemagick', fps=30)  # Save the animation as a GIF file

# Show the animation
plt.show()  # Display the animation in a window
