import os
import pygame
import pymunk
import pymunk.pygame_util
import pygad
from PIL import Image  # For saving animation as a GIF

# The goal of this genetic algorithm is to find the smallest box three falling bouncy balls can fit in.
# Any solutions such that the balls fall out of the box are invalid.
# This program demonstrates how pygad and pymunk, a 2D physics engine, can be used to generate static bodies.


def simulate_falling_balls(ga_instance, solution, solution_idx, *args):
    """Simulates three balls falling into a box and returns the sum of their y-coordinates.

    Args:
        solution: box width and height
    *Args:
        draw (bool): Whether to render the simulation using Pygame.
        save_animation (bool): Whether to save frames as images for creating an animation.

    Returns:
        float: Fitness score for the genetic algorithm.
    """

    width, height = 800, 600  # Screen dimensions

    # Extract dimensions from the solution
    box_width = solution[0]
    box_height = solution[1]

    # Extract *args if provided
    if args:
        draw = args[0]
        save_animation = args[1]
    else:
        draw = False
        save_animation = False

    # === Initialize Pygame (only if drawing is enabled) ===
    if draw or save_animation:
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()

        # Create folder for saving animation frames
        if save_animation and not os.path.exists("pymunk_box"):
            os.makedirs("pymunk_box")

    # === Initialize Pymunk Space ===
    space = pymunk.Space()
    space.gravity = (0, 900)  # Gravity pulling down

    # === Create the Box (Static Walls) ===
    box_x = 400  # Keep the box centered horizontally
    box_y = (height - 100) - box_height  # Ensure the bottom of the box is always at y = 100

    # Define the three walls of the box (bottom, left, right)
    walls = [
        pymunk.Segment(space.static_body, (box_x - box_width // 2, height - 100),
                       (box_x + box_width // 2, height - 100), 5),  # Bottom
        pymunk.Segment(space.static_body, (box_x - box_width // 2, height - 100), (box_x - box_width // 2, box_y), 5),
        # Left
        pymunk.Segment(space.static_body, (box_x + box_width // 2, height - 100), (box_x + box_width // 2, box_y), 5),
        # Right
    ]

    for wall in walls:
        wall.elasticity = 0.5  # Some bounce
        space.add(wall)

    # === Create Three Balls ===
    ball_mass, ball_radius = 5, 20
    ball_positions = [(370, 100), (400, 50), (430, 80)]  # Initial positions for three balls

    balls = []
    for pos in ball_positions:
        moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
        ball_body = pymunk.Body(ball_mass, moment)
        ball_body.position = pos

        ball_shape = pymunk.Circle(ball_body, ball_radius)
        ball_shape.elasticity = 1  # Bouncy

        space.add(ball_body, ball_shape)
        balls.append(ball_body)

    # === Pygame Draw Options ===
    if draw or save_animation:
        draw_options = pymunk.pygame_util.DrawOptions(screen)

    # === Simulation Loop ===
    frames = []  # Store frames for GIF
    for frame_num in range(300):  # Simulate for 5 seconds (assuming 60 FPS)
        space.step(1 / 60.0)  # Step physics simulation

        # Store ball coordinates
        ball_positions = [height - ball.position.y for ball in balls]

        if draw or save_animation:
            screen.fill((255, 255, 255))  # Clear screen
            space.debug_draw(draw_options)  # Draw objects

            if save_animation:
                filename = f"pymunk_box/frame_{frame_num:03d}.png"
                pygame.image.save(screen, filename)  # Save each frame
                frames.append(filename)

            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS

    if draw or save_animation:
        pygame.quit()
        print("Ball positions:", ball_positions)

    # === Generate GIF if enabled ===
    if save_animation:
        print("Saving animation as GIF...")
        images = [Image.open(f) for f in frames]
        images[0].save("pymunk_box/simulation.gif", save_all=True, append_images=images[1:], duration=16, loop=0)
        print("Animation saved as pymunk_box/simulation.gif")

        # Cleanup: Delete individual frame PNGs
        for frame in frames:
            try:
                os.remove(frame)
            except OSError as e:
                print(f"Error deleting {frame}: {e}")

    # === Compute Fitness ===
    fitness = 1 / (box_width * box_height)  # Fitness grows as volume shrinks
    for pos in ball_positions:
        if pos < 100:
            fitness = 0  # Invalidate solution by assigning zero fitness if balls fall out

    return fitness  # Return fitness (minimize volume)


# Set parameters for the genetic algorithm
num_generations = 500  # The number of generations the GA will run
num_parents_mating = 4  # The number of parents selected for mating
sol_per_pop = 20  # Number of solutions in each population
num_genes = 2  # Number of genes (dimensions)
init_range_low = 10  # The lower bound for box dimensions
init_range_high = 1000  # The upper bound for box dimensions

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
    fitness_func=simulate_falling_balls,  # Assign the fitness function
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

# Print best solution
print("Best polynomial coefficients: width={}, height={}".format(solution[0], solution[1]))

simulate_falling_balls(None, solution, solution_idx, True, True)  # Simulate + draw + save best solution

# simulate_falling_balls(None, [100, 200], solution_idx, True, True)  # Simulate + draw + save some solution (test)
