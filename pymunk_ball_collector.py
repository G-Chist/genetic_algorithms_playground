import math
import random

import pygame
import pymunk
import pymunk.pygame_util
import pygad
import os
from PIL import Image  # For saving animation as a GIF


width, height = 900, 600  # Screen dimensions


def simulate_balls(ga_instance, solution, solution_idx, *args):

    # Extract *args if provided
    if args:
        draw = args[0]
        save_animation = args[1]
    else:
        draw = False
        save_animation = False

    # Extract solution if provided, otherwise use default
    if solution is not None:
        arm_solution = solution[0]
        w_solution = solution[1]
        points_solution = solution[2:]
    else:
        arm_solution = 250
        w_solution = 7
        points_solution = [500, height - 70,
                           575, height - 125,
                           640, height - 180,
                           620, height - 125,
                           580, height - 70,
                           735, height - 70,
                           880, height - 70,
                           870, height - 185,
                           880, height - 300,
                           725, height - 310,
                           550, height - 300]

    # === Initialize Pygame (only if drawing is enabled) ===
    if draw or save_animation:
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()

        # Create folder for saving animation frames
        if save_animation and not os.path.exists("pymunk_ball_collector"):
            os.makedirs("pymunk_ball_collector")

    # === Initialize Pymunk Space ===
    space = pymunk.Space()
    space.gravity = (0, 900)  # Gravity pulling down

    # Create ground
    floor = pymunk.Segment(space.static_body, (-100, height - 50), (width, height - 50), 5)
    floor.elasticity = 0
    space.add(floor)

    # Create static components (slope)
    static_body = space.static_body
    static_lines = [
        pymunk.Segment(static_body, (0, height - 160), (200, height - 50), 5),
    ]
    for line in static_lines:
        line.elasticity = 0
        line.friction = 0.9
    space.add(*static_lines)  # all elements of static_lines

    # === Create Balls ===
    ball_mass, ball_radius = 5, 25
    ball_x = 50
    # 12 balls in total
    ball_positions = [(ball_x, height - 500), (ball_x, height - 550), (ball_x, height - 600), (ball_x, height - 650),
                      (ball_x, height - 700), (ball_x, height - 750), (ball_x, height - 800), (ball_x, height - 850),
                      (ball_x, height - 900), (ball_x, height - 950), (ball_x, height - 1000), (ball_x, height - 1050)]

    balls = []
    for pos in ball_positions:
        # Define random increment for radius
        # random_increment = random.randint(-5, 5)
        random_increment = 0
        moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius + random_increment)
        ball_body = pymunk.Body(ball_mass, moment)
        ball_body.position = pos

        ball_shape = pymunk.Circle(ball_body, ball_radius + random_increment)
        ball_shape.elasticity = 0.5  # Bouncy

        space.add(ball_body, ball_shape)
        balls.append(ball_body)

    # Define motor position
    x_rot = 400
    y_rot = height-200

    # Define arm parameters
    length = arm_solution

    # Define motor angular speed
    w = w_solution

    # ----- Create rotating stick -----
    body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    body.position = x_rot, y_rot
    shape = pymunk.Segment(body, (-length/2, 0), (length/2, 0), 5)  # Centered on the joint
    shape.density = 1
    space.add(body, shape)

    # ----- Pin to center -----
    pivot = pymunk.PivotJoint(space.static_body, body, (x_rot, y_rot))
    space.add(pivot)

    # ----- Add motor -----
    motor = pymunk.SimpleMotor(space.static_body, body, w)
    space.add(motor)

    # Create static components (collector)
    static_body = space.static_body

    static_lines_collector = [
        pymunk.Segment(static_body, (points_solution[i], points_solution[i+1]), (points_solution[i+2], points_solution[i+3]), 5)
        for i in range(0, len(points_solution)-3, 2)
    ]

    for line in static_lines_collector:
        line.elasticity = 0
        line.friction = 0.9
    space.add(*static_lines_collector)  # all elements of static_lines_collector

    # Compute total distance between consecutive point pairs to evaluate resource cost
    total_distance = 0
    for i in range(0, len(points_solution) - 2, 2):  # step by 2, avoid last->first
        x1, y1 = points_solution[i], points_solution[i + 1]
        x2, y2 = points_solution[i + 2], points_solution[i + 3]
        dist = math.hypot(x2 - x1, y2 - y1)
        total_distance += dist

    # === Pygame Draw Options ===
    if draw or save_animation:
        draw_options = pymunk.pygame_util.DrawOptions(screen)

    # === Simulation Loop ===
    frames = []  # Store frames for GIF
    for frame_num in range(600):  # (assuming 60 FPS)
        space.step(1 / 60.0)  # Step physics simulation

        # Store ball coordinates
        ball_positions = [(ball.position.x, height - ball.position.y) for ball in balls]

        if draw or save_animation:
            screen.fill((255, 255, 255))  # Clear screen
            space.debug_draw(draw_options)  # Draw objects

            if save_animation:
                filename = f"pymunk_ball_collector/frame_{frame_num:03d}.png"
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
        images[0].save("pymunk_ball_collector/simulation.gif", save_all=True, append_images=images[1:], duration=16, loop=0)
        print("Animation saved as pymunk_ball_collector/simulation.gif")

        # Cleanup: Delete individual frame PNGs
        for frame in frames:
            try:
                os.remove(frame)
            except OSError as e:
                print(f"Error deleting {frame}: {e}")

    # === Compute Fitness ===
    fitness = 0

    for position in ball_positions:
        if position[0] > 580 and 70 < position[1] < 310:  # x > 580, y between 70 and 310
            fitness += 1000  # 1000 fitness per ball in box

    # Less material used for box => better fitness
    # Less motor power used => better fitness
    k_w = 0.1
    k_distance = 0.1
    fitness -= total_distance * k_distance
    fitness -= w*k_w

    if draw:
        print(f"Fitness: {fitness}")
        print(f"Total distance: {total_distance}")

    return fitness


# simulate_balls(None, None, None, True, False)  # Example call, draw and don't save gif

# GENES:
# motor speed
# arm length
# box joint coordinates (11 x 2)

# Set parameters for the genetic algorithm
num_generations = 100  # The number of generations the GA will run
num_parents_mating = 4  # The number of parents selected for mating
sol_per_pop = 20  # Number of solutions in each population
num_genes = 1 + 1 + 11 * 2  # Number of genes

# Different ranges for each gene
gene_space = [
    {"low": 20, "high": 256},  # Gene 1: arm length
    {"low": 2, "high": 20},    # Gene 2: motor speed
]

# Start from the third gene — the coordinates
original_coords = [
    (500, height - 70),
    (575, height - 125),
    (640, height - 180),
    (620, height - 125),
    (580, height - 70),
    (735, height - 70),
    (880, height - 70),
    (870, height - 185),
    (880, height - 300),
    (725, height - 310),
    (550, height - 300)
]

# Add coordinate ranges with small variation
for x, y in original_coords:
    gene_space.append({"low": x - 20, "high": x + 20})
    gene_space.append({"low": y - 15, "high": y + 15})


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
    fitness_func=simulate_balls,  # Assign the fitness function
    sol_per_pop=sol_per_pop,  # Set the number of solutions per population
    num_genes=num_genes,  # Set the number of genes
    gene_space=gene_space,  # Custom gene limits
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
print("Best solution: ")
print(solution)

simulate_balls(None, solution, solution_idx, True, True)  # Simulate + draw + save best solution
