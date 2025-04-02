import os
import pygame
import pymunk
import pymunk.pygame_util
import pygad
import math
import numpy as np
from random import randint, uniform
from PIL import Image  # For saving animation as a GIF
from matplotlib import pyplot


def sigmoid(x):
    """
    Args:
        x: any number

    Returns: 1 / (1 + e^(-x))
    """
    return 1 / (1 + np.exp(-np.clip(x, -5000, 5000)))  # Clip to prevent overflow


def neural_network(boxX, boxY, wm11, wm21, bm1, bm2, wo11, wo12, bo1, bo2):
    """
    2-input, 2-hidden neuron, 2-output neural network.
    Inputs: boxX, boxY
    Outputs: angle, speed
    """
    hidden1 = sigmoid(wm11 * boxX + wm21 * boxY + bm1)
    hidden2 = sigmoid(wm11 * boxX + wm21 * boxY + bm2)

    angle = 20 + sigmoid(wo11 * hidden1 + wo12 * hidden2 + bo1) * 70  # Map to 20-90 degrees
    speed = 500 + sigmoid(wo11 * hidden1 + wo12 * hidden2 + bo2) * 1500  # Map to 500-2000 units

    return angle, speed


def throw_ball_simulation(ga_instance, solution, solution_idx, x=100, y=500, random_input=True, draw=False, save_animation=False, *args):
    """
    Simulates a ball being thrown.
    """

    fitness = 0

    for _ in range(10):  # Simulate 10 random points
        width, height = 800, 600  # Screen size

        box_height = 100
        box_width = 100

        # Extract NN weights & biases
        wm11, wm21, bm1, bm2, wo11, wo12, bo1, bo2 = solution

        # Randomize box positions
        if random_input:
            boxX = np.random.uniform(350, 450)
            boxY = np.random.uniform(50, 200)
        else:
            if args:  # Pass position as *args
                boxX = args[0]
                boxY = args[1]
            else:
                raise ValueError

        # Use NN to get angle and speed
        angle_degrees, speed = neural_network(boxX, boxY, wm11, wm21, bm1, bm2, wo11, wo12, bo1, bo2)

        if draw:
            print(f"Inputs: {boxX}, {boxY}")
            print(f"Angle: {angle_degrees:.5f}, speed: {speed:.5f}")

        # Convert angle to radians and compute velocity components
        angle_radians = math.radians(angle_degrees)
        vx = math.cos(angle_radians) * speed
        vy = -math.sin(angle_radians) * speed  # Negative because Y-axis is downward in Pygame

        # Initialize Pygame (if drawing or saving animation)
        if draw or save_animation:
            pygame.init()
            screen = pygame.display.set_mode((width, height))
            clock = pygame.time.Clock()

            if save_animation and not os.path.exists("pymunk_throw"):
                os.makedirs("pymunk_throw")

        # Initialize Pymunk physics engine
        space = pymunk.Space()
        space.gravity = (0, 980)  # Gravity in pixels per second squared

        # Create ground
        floor = pymunk.Segment(space.static_body, (0, height - 50), (width, height - 50), 5)
        floor.elasticity = 0.8
        space.add(floor)

        # === Create the Box (Static Walls) ===
        box_x = boxX
        box_ystart = boxY
        box_y = (height - box_ystart) - box_height  # Ensure the bottom of the box is always at y = box_ystart

        # Define the three walls of the box (bottom, left, right)
        walls = [
            pymunk.Segment(space.static_body, (box_x - box_width // 2, height - box_ystart),
                           (box_x + box_width // 2, height - box_ystart), 5),  # Bottom
            pymunk.Segment(space.static_body, (box_x - box_width // 2, height - box_ystart), (box_x - box_width // 2, box_y), 5),
            # Left
            pymunk.Segment(space.static_body, (box_x + box_width // 2, height - box_ystart), (box_x + box_width // 2, box_y), 5),
            # Right
        ]

        for wall in walls:
            wall.elasticity = 0.5  # Some bounce
            space.add(wall)

        # Create ball
        ball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
        ball_body.position = x, y
        ball_body.velocity = vx, vy

        ball_shape = pymunk.Circle(ball_body, 15)
        ball_shape.elasticity = 0.8
        space.add(ball_body, ball_shape)

        # Draw options for visualization
        if draw or save_animation:
            draw_options = pymunk.pygame_util.DrawOptions(screen)

        # Simulation loop
        frames = []
        ball_positions = []

        for frame_num in range(360):  # Assuming 60 FPS
            space.step(1 / 60.0)  # Step physics simulation
            ball_positions.append((ball_body.position.x, height - ball_body.position.y))  # Store position

            if draw or save_animation:
                screen.fill((0, 0, 0))  # Clear screen
                space.debug_draw(draw_options)  # Draw objects

                if save_animation:
                    filename = f"pymunk_throw/frame_{frame_num:03d}.png"
                    pygame.image.save(screen, filename)
                    frames.append(filename)

                pygame.display.flip()
                clock.tick(60)

        if draw or save_animation:
            pygame.quit()

        # Generate GIF if enabled
        if save_animation:
            print("Saving animation as GIF...")
            images = [Image.open(f) for f in frames]
            images[0].save("pymunk_throw/throw_simulation.gif", save_all=True, append_images=images[1:], duration=1, loop=0)
            print("Animation saved as pymunk_throw/throw_simulation.gif")

            # Cleanup frames
            for frame in frames:
                os.remove(frame)

        # Compute square of distance from the box for fitness function
        x_diff = (ball_body.position.x - boxX)
        y_diff = (ball_body.position.y - boxY + box_height//2)
        dist_from_box = x_diff*x_diff + y_diff*y_diff

        # If ball is in box, return 10000 + speed*k1 + angle*k2 as fitness
        if (boxX - box_width // 2) <= ball_body.position.x <= (boxX + box_width // 2) and (height - boxY - box_height) <= ball_body.position.y <= (height - boxY):
            # print("Ball successfully landed inside the box!")
            fitness += 10000 - speed*0.1 + angle_degrees*4

        fitness += 1 / dist_from_box

    return fitness


# Set parameters for the genetic algorithm
num_generations = 300  # The number of generations the GA will run
num_parents_mating = 4  # The number of parents selected for mating
sol_per_pop = 50  # Number of solutions in each population
num_genes = 8  # Neural network parameters (weights and biases)
gene_space = [{"low": -0.5, "high": 0.5} for _ in range(num_genes)]  # Weight and bias range

# Set the types of parent selection, crossover, and mutation methods
parent_selection_type = "random"
keep_parents = 2  # Number of parents to keep from one generation to the next
crossover_type = "single_point"  # Single-point crossover method is used to combine parent solutions
mutation_type = "random"  # Random mutation method will be used to introduce variation
mutation_percent_genes = 30  # Percentage of genes that will undergo mutation in each generation

# Initialize the genetic algorithm instance with all the parameters
ga_instance = pygad.GA(
    num_generations=num_generations,  # Set number of generations
    num_parents_mating=num_parents_mating,  # Set number of parents mating
    fitness_func=lambda ga, sol, idx: throw_ball_simulation(ga, sol, idx),  # Assign the fitness function
    sol_per_pop=sol_per_pop,  # Set the number of solutions per population
    num_genes=num_genes,  # Set the number of genes
    gene_space=gene_space,
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
print(f"Best solution: ", end="")
print(solution)
print(f"Best solution fitness: {solution_fitness}")

throw_ball_simulation(None, solution, solution_idx, draw=True)  # Simulate + draw best solution
throw_ball_simulation(None, solution, solution_idx, draw=True)  # Simulate + draw best solution
