import random

import pygame
import pymunk
import pymunk.pygame_util
import pygad
import os
from PIL import Image  # For saving animation as a GIF


def simulate_balls(ga_instance, solution, solution_idx, *args):

    width, height = 900, 600  # Screen dimensions

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
        random_increment = random.randint(-5, 5)
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
    length = 255

    # Define motor angular speed
    w = 7

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
        # Sloped line with midpoint
        pymunk.Segment(static_body, (500, height - 70), (575, height - 125), 5),
        pymunk.Segment(static_body, (575, height - 125), (640, height - 180), 5),

        # Downward slope back up with midpoint
        pymunk.Segment(static_body, (640, height - 180), (620, height - 125), 5),
        pymunk.Segment(static_body, (620, height - 125), (580, height - 70), 5),

        # Flat section split into two
        pymunk.Segment(static_body, (580, height - 70), (735, height - 70), 5),
        pymunk.Segment(static_body, (735, height - 70), (880, height - 70), 5),

        # Vertical section split
        pymunk.Segment(static_body, (880, height - 70), (870, height - 185), 5),
        pymunk.Segment(static_body, (870, height - 185), (880, height - 300), 5),

        # Top segment with midpoint
        pymunk.Segment(static_body, (880, height - 300), (725, height - 310), 5),
        pymunk.Segment(static_body, (725, height - 310), (550, height - 300), 5),
    ]

    for line in static_lines_collector:
        line.elasticity = 0
        line.friction = 0.9
    space.add(*static_lines_collector)  # all elements of static_lines_collector

    # === Pygame Draw Options ===
    if draw or save_animation:
        draw_options = pymunk.pygame_util.DrawOptions(screen)

    # === Simulation Loop ===
    frames = []  # Store frames for GIF
    for frame_num in range(900):  # (assuming 60 FPS)
        space.step(1 / 60.0)  # Step physics simulation

        # Store ball coordinates
        ball_positions = [height - ball.position.y for ball in balls]

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

    return fitness


simulate_balls(None, None, None, True, False)  # Example call, draw and don't save gif
