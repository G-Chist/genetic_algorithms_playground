import pygame
import pymunk
import pymunk.pygame_util
import pygad
import os
from PIL import Image  # For saving animation as a GIF


def simulate_balls(ga_instance, solution, solution_idx, *args):

    width, height = 800, 600  # Screen dimensions

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


    # === Create Ball ===
    ball_mass, ball_radius = 5, 20
    ball_positions = [(100, 100)]

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


simulate_balls(None, None, None, True, True)  # Example call, draw and save gif
