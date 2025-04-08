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
    floor = pymunk.Segment(space.static_body, (0, height - 50), (width, height - 50), 5)
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
    space.add(*static_lines)

    # === Create Balls ===
    ball_mass, ball_radius = 5, 20
    ball_x = 50
    ball_positions = [(ball_x, height - 500), (ball_x, height - 550), (ball_x, height - 600), (ball_x, height - 650),
                      (ball_x, height - 700), (ball_x, height - 750), (ball_x, height - 800), (ball_x, height - 850)]

    balls = []
    for pos in ball_positions:
        moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
        ball_body = pymunk.Body(ball_mass, moment)
        ball_body.position = pos

        ball_shape = pymunk.Circle(ball_body, ball_radius)
        ball_shape.elasticity = 1  # Bouncy

        space.add(ball_body, ball_shape)
        balls.append(ball_body)

    # Define motor position
    x_rot = 600
    y_rot = height-200

    # Define arm parameter
    length = 50

    # Define motor angular speed
    w = 10

    # ----- Create rotating stick -----
    body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    body.position = x_rot, y_rot
    shape = pymunk.Segment(body, (0, 0), (length, 0), 5)  # stick extends right
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
    for frame_num in range(300):  # (assuming 60 FPS)
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
