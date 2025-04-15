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
    shape.density = 0.1
    space.add(body, shape)

    # ----- Pin to center -----
    pivot = pymunk.PivotJoint(space.static_body, body, (x_rot, y_rot))
    space.add(pivot)

    motor = pymunk.SimpleMotor(space.static_body, body, w)
    motor.max_force = 15000  # Limit torque so as not to break joints
    space.add(motor)
    direction = 1  # 1 for forward, -1 for reverse

    # === Create connecting rod ===
    rod_length = 150
    rod_body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    rod_body.position = x_rot + length, y_rot  # attach to crank end
    rod_shape = pymunk.Segment(rod_body, (0, 0), (0, rod_length), 4)
    rod_shape.density = 0.1
    space.add(rod_body, rod_shape)

    # ----- Connect rod to crank end -----
    rod_joint_to_crank = pymunk.PinJoint(body, rod_body, (length, 0), (0, 0))
    space.add(rod_joint_to_crank)

    # === Create piston ===
    piston_body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    piston_body.position = x_rot + length, y_rot + rod_length
    piston_shape = pymunk.Poly.create_box(piston_body, size=(100, 20))
    piston_shape.density = 0.1
    space.add(piston_body, piston_shape)

    # ----- Connect rod to piston -----
    rod_joint_to_piston = pymunk.PinJoint(rod_body, piston_body, (0, rod_length), (0, 0))
    space.add(rod_joint_to_piston)

    # Get piston width
    piston_width = 100

    # Define groove vertical range
    groove_top_y = y_rot + 100
    groove_bottom_y = y_rot + 400

    # ----- Left-side groove joint -----
    left_groove = pymunk.GrooveJoint(space.static_body, piston_body,
                                     (x_rot + length - piston_width / 2, groove_top_y),
                                     (x_rot + length - piston_width / 2, groove_bottom_y),
                                     (-piston_width / 2, 0))  # anchor on piston
    space.add(left_groove)

    # ----- Right-side groove joint -----
    right_groove = pymunk.GrooveJoint(space.static_body, piston_body,
                                      (x_rot + length + piston_width / 2, groove_top_y),
                                      (x_rot + length + piston_width / 2, groove_bottom_y),
                                      (piston_width / 2, 0))  # anchor on piston
    space.add(right_groove)

    rod_joint_to_crank.stiffness = 1e6
    rod_joint_to_crank.damping = 1e4

    rod_joint_to_piston.stiffness = 1e6
    rod_joint_to_piston.damping = 1e4

    left_groove.stiffness = 1e6
    left_groove.damping = 1e4

    right_groove.stiffness = 1e6
    right_groove.damping = 1e4

    # === Pygame Draw Options ===
    if draw or save_animation:
        draw_options = pymunk.pygame_util.DrawOptions(screen)

    # === Simulation Loop ===
    frames = []  # Store frames for GIF
    for frame_num in range(400):  # (assuming 60 FPS)
        space.step(1 / 60.0)  # Step physics simulation

        # Get angle in degrees
        angle_deg = math.degrees(body.angle)

        # Check constraints
        if angle_deg >= 30 and direction == 1:
            direction = -1
            motor.rate = direction * w
        elif angle_deg <= -20 and direction == -1:
            direction = 1
            motor.rate = direction * w

        if draw or save_animation:
            screen.fill((255, 255, 255))  # Clear screen
            space.debug_draw(draw_options)  # Draw objects
            # print(f"Motor arm angle: {math.degrees(body.angle):.2f} degrees")

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
