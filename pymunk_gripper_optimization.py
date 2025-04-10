import math
import random

import pygame
import pymunk
import pymunk.pygame_util
import pygad
import os
from PIL import Image  # For saving animation as a GIF

width, height = 900, 600  # Screen dimensions

def simulate_gripper(ga_instance, solution, solution_idx, *args):

    # Extract *args if provided
    if args:
        draw = args[0]
        save_animation = args[1]
    else:
        draw = False
        save_animation = False

    # Extract solution if provided, otherwise use default
    if solution is not None:
        gripper_shape = solution
    else:
        gripper_shape = [0 for _ in range(30)]

    # === Initialize Pygame (only if drawing is enabled) ===
    if draw or save_animation:
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()

        # Create folder for saving animation frames
        if save_animation and not os.path.exists("pymunk_gripper_optimization"):
            os.makedirs("pymunk_gripper_optimization")

    # === Initialize Pymunk Space ===
    space = pymunk.Space()
    space.gravity = (0, 900)  # Gravity pulling down

    # Create ground
    floor = pymunk.Segment(space.static_body, (-100, height - 20), (width, height - 20), 5)
    floor.elasticity = 0
    space.add(floor)

    # Define motor position
    x_rot = 400
    y_rot = height - 400

    # Define arm parameters
    length = 200

    # Define motor angular speed
    w = 7

    # ----- Create rotating stick -----
    body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    body.position = x_rot, y_rot
    shape = pymunk.Segment(body, (length, 0), (-5/2, 0), 5)  # Centered on the joint
    shape.density = 1
    space.add(body, shape)

    # ----- Pin to center -----
    pivot = pymunk.PivotJoint(space.static_body, body, (x_rot, y_rot))
    space.add(pivot)

    # ----- Add motor -----
    motor = pymunk.SimpleMotor(space.static_body, body, w)
    space.add(motor)

    # === Pygame Draw Options ===
    if draw or save_animation:
        draw_options = pymunk.pygame_util.DrawOptions(screen)

    # === Simulation Loop ===
    frames = []  # Store frames for GIF
    for frame_num in range(400):  # (assuming 60 FPS)
        space.step(1 / 60.0)  # Step physics simulation

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

    # === Generate GIF if enabled ===
    if save_animation:
        print("Saving animation as GIF...")
        images = [Image.open(f) for f in frames]
        images[0].save("pymunk_ball_collector/simulation.gif", save_all=True, append_images=images[1:], duration=16,
                       loop=0)
        print("Animation saved as pymunk_ball_collector/simulation.gif")

        # Cleanup: Delete individual frame PNGs
        for frame in frames:
            try:
                os.remove(frame)
            except OSError as e:
                print(f"Error deleting {frame}: {e}")

    # === Compute Fitness ===
    fitness = 0

    if draw:
        print(f"Fitness: {fitness}")

    return fitness


simulate_gripper(None, None, None, True, False)  # Example call
