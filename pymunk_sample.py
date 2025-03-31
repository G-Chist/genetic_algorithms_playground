import pygame
import pymunk
import pymunk.pygame_util


def simulate_falling_balls(box_width, box_height, draw=False):
    """Simulates three balls falling into a box and returns the sum of their y-coordinates.

    Args:
        box_width (int): Width of the box.
        box_height (int): Height of the box.
        draw (bool): Whether to render the simulation using Pygame.

    Returns:
        float: Sum of the y-coordinates of the three balls at the end of simulation.
    """

    width, height = 800, 600  # Screen dimensions

    # === Initialize Pygame (only if drawing is enabled) ===
    if draw:
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()

    # === Initialize Pymunk Space ===
    space = pymunk.Space()
    space.gravity = (0, 900)  # Gravity pulling down

    # === Create the Box (Static Walls) ===
    box_x, box_y = 400, 500  # Box position (center)

    # Define the three walls of the box (bottom, left, right)
    walls = [
        pymunk.Segment(space.static_body, (box_x - box_width // 2, box_y), (box_x + box_width // 2, box_y), 5),
        # Bottom
        pymunk.Segment(space.static_body, (box_x - box_width // 2, box_y), (box_x - box_width // 2, box_y - box_height),
                       5),  # Left
        pymunk.Segment(space.static_body, (box_x + box_width // 2, box_y), (box_x + box_width // 2, box_y - box_height),
                       5),  # Right
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
    if draw:
        draw_options = pymunk.pygame_util.DrawOptions(screen)

    # === Simulation Loop ===
    for _ in range(300):  # Simulate for 5 seconds (assuming 60 FPS)
        space.step(1 / 60.0)  # Step physics simulation

        # Sum ball coordinates
        ball_positions_sum = sum(height-ball.position.y for ball in balls)

        if draw:
            screen.fill((255, 255, 255))  # Clear screen
            space.debug_draw(draw_options)  # Draw objects
            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS

    if draw:
        pygame.quit()

    return ball_positions_sum  # Return sum of the y-coordinates


# Example usage:
result = simulate_falling_balls(200, 100, draw=False)
print("Sum of ball y-coordinates:", result)
