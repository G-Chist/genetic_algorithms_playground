import random  # For generating random values
import math  # For mathematical operations
import numpy as np  # For numerical operations (arrays, range generation)
import matplotlib.pyplot as plt  # For plotting graphs
import matplotlib.animation as animation  # For creating animated visualizations


# Define the polynomial function (cubic equation)
def polynomial(a, b, c, d, x):
    """
    Computes the value of a cubic polynomial: a*x^3 + b*x^2 + c*x + d

    Parameters:
    a, b, c, d: coefficients of the polynomial
    x: input value

    Returns:
    The computed polynomial value at x
    """
    return a * (x ** 3) + b * (x * x) + c * x + d


# Define the fitness function to evaluate how well a polynomial approximates a target function
def fitness_function(a, b, c, d, function_to_approximate, start=-2, end=2, step=0.05):
    """
    Calculates the fitness score of a polynomial by measuring its error in approximating
    the target function over a specified range.

    Parameters:
    a, b, c, d: polynomial coefficients
    function_to_approximate: the target function to approximate (e.g., math.sin)
    start, end: range of x values over which to compare the function
    step: step size for x values in the range

    Returns:
    A fitness score (higher is better). The score is the inverse of the accumulated error.
    """
    accumulated_error = sum(
        abs(polynomial(a, b, c, d, x) - function_to_approximate(x))
        for x in np.arange(start, end, step)
    )
    return 1 / abs(accumulated_error)  # Lower error results in a higher fitness score


# Function to generate a random individual (random polynomial coefficients)
def generate_individual():
    """
    Creates a random set of coefficients for a cubic polynomial.

    Returns:
    A tuple (a, b, c, d) with random values.
    """
    return random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-0.1, 0.1)


# Function to generate an initial population of random individuals
def generate_population(size):
    """
    Generates an initial population of individuals (random cubic polynomials).

    Parameters:
    size: number of individuals in the population

    Returns:
    A list of individuals (tuples of coefficients).
    """
    return [generate_individual() for _ in range(size)]


# Tournament selection function for choosing parents
def tournament_selection(population, fitness_scores, k=2):
    """
    Selects a parent from the population using tournament selection.

    Parameters:
    population: list of individuals
    fitness_scores: list of fitness scores corresponding to individuals
    k: number of randomly chosen individuals to compete in the tournament

    Returns:
    The best individual among the selected competitors.
    """
    selected = random.sample(list(zip(population, fitness_scores)), k)
    return max(selected, key=lambda x: x[1])[0]  # Select individual with highest fitness


# Function to perform crossover between two parent individuals
def crossover(parent1, parent2):
    """
    Performs one-point crossover to generate two offspring.

    Parameters:
    parent1, parent2: tuples representing two parent individuals

    Returns:
    Two new child individuals created by swapping parts of the parents.
    """
    crossover_point = random.randint(1, 3)  # Choose a crossover index (1 to 3)
    return (
        parent1[:crossover_point] + parent2[crossover_point:],
        parent2[:crossover_point] + parent1[crossover_point:]
    )


# Function to apply mutation to an individual
def mutate(individual, mutation_rate=0.35):
    """
    Mutates an individual by slightly modifying one of its coefficients.

    Parameters:
    individual: tuple of polynomial coefficients
    mutation_rate: probability of applying a mutation

    Returns:
    A mutated individual (or the same individual if no mutation occurs).
    """
    if random.random() < mutation_rate:  # Apply mutation with given probability
        index = random.randint(0, 3)  # Choose a random coefficient to mutate
        mutated = list(individual)
        mutated[index] *= random.uniform(0.8, 1.2)  # Apply a small random change
        return tuple(mutated)
    return individual  # Return original if no mutation occurs


# Genetic algorithm to evolve a polynomial approximation
def generate_evolution(population_size, max_generations, function_to_approximate, step_frequency=20):
    """
    Evolves a population of polynomials to approximate a given function using a genetic algorithm.

    Parameters:
    population_size: number of individuals in the population
    max_generations: number of generations to evolve
    function_to_approximate: the function being approximated (e.g., math.sin)
    step_frequency: how often to store the best solution for visualization

    Returns:
    A list of the best individuals at different points in evolution.
    """
    population = generate_population(population_size)  # Generate initial population
    evolution = []  # Store best individuals at specific intervals

    for generation in range(max_generations):
        # Compute fitness scores for all individuals
        fitness_scores = [fitness_function(*ind, function_to_approximate) for ind in population]
        # Use *ind to unpack tuple

        # Identify the best individual in the population
        best_individual = population[fitness_scores.index(max(fitness_scores))]

        # Store the best individual at specified intervals for animation
        if generation % step_frequency == 0:
            evolution.append(best_individual)

        # Generate next generation through selection, crossover, and mutation
        next_generation = []
        while len(next_generation) < population_size:
            parent1 = tournament_selection(population, fitness_scores)
            parent2 = tournament_selection(population, fitness_scores)
            child1, child2 = crossover(parent1, parent2)
            next_generation.append(mutate(child1))
            if len(next_generation) < population_size:
                next_generation.append(mutate(child2))

        population = next_generation  # Update population

    return evolution  # Return the stored best individuals over time


# Function to animate the polynomial evolution
def animate_polynomial_approximation(function_to_approximate, population_size=50, max_generations=1000):
    """
    Runs the genetic algorithm and animates the evolution of polynomial approximations.

    Parameters:
    function_to_approximate: the target function (e.g., math.sin)
    population_size: number of individuals in the population
    max_generations: total number of generations

    Returns:
    Animated visualization of the evolution process.
    """
    # Run the genetic algorithm
    evolution = generate_evolution(population_size, max_generations, function_to_approximate, step_frequency=20)

    # Set up the plot
    fig, ax = plt.subplots()
    x_values = np.linspace(-5, 5, 500)
    y_function = np.vectorize(function_to_approximate)(x_values)
    line, = ax.plot(x_values, np.zeros_like(x_values), label="Evolving Polynomial", color="red")

    # Configure plot aesthetics
    ax.plot(x_values, y_function, label=function_to_approximate.__name__, color="blue")
    ax.set_xlim(-5, 5)
    ax.set_ylim(-1.5, 1.5)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    ax.set_title(f"Evolution of Polynomial Approximation of {function_to_approximate.__name__}")

    # Define the update function for animation
    def update(frame):
        """Updates the plot with the current best polynomial."""
        best_individual = evolution[frame]
        y_poly = polynomial(*best_individual, x_values)
        line.set_ydata(y_poly)
        return line,

    # Create animation
    ani = animation.FuncAnimation(fig, update, frames=len(evolution), interval=50, repeat=False)

    # Save the animation as a GIF (optional)
    ani.save(f'polynomial_approximation_{function_to_approximate.__name__}.gif', writer='imagemagick', fps=30)

    # Show the animation
    plt.show()


def x_square(x):
    return x*x


# Run the algorithm to approximate x^2
animate_polynomial_approximation(x_square)
