import pygame  # Pygame for visualization
import pymunk  # Pymunk for physics simulation
import pymunk.pygame_util  # Pymunk utility for drawing
import numpy as np  # Numpy for numerical operations

# === Initialize Pygame ===
pygame.init()  # Initialize Pygame
width, height = 800, 600  # Define screen dimensions
# screen = pygame.display.set_mode((width, height))  # Create Pygame window
clock = pygame.time.Clock()  # Create a clock for frame rate control

# === Initialize Pymunk Space ===
space = pymunk.Space()  # Create a Pymunk physics simulation space
space.gravity = (0, 900)  # Set gravity (pulling objects down)


# === Function defining the curve (polynomial) ===
def polynomial(x):
    """Defines a function to generate the curved surface.
    """
    return 0.002 * (x ** 2) - 0.8 * x + 300


# === Create the static ground based on the polynomial function ===
curve_points = []  # List to store curve segments
num_points = 50  # Number of points to approximate the curve
x_values = np.linspace(50, 350, num_points)  # Generate evenly spaced x values

# Loop through x values and create segments
for i in range(len(x_values) - 1):
    x1, x2 = x_values[i], x_values[i + 1]  # Get two consecutive x values
    y1, y2 = polynomial(x1), polynomial(x2)  # Compute corresponding y values

    # Create a static body (no mass, does not move)
    body = pymunk.Body(body_type=pymunk.Body.STATIC)

    # Create a segment between the two points
    segment = pymunk.Segment(body, (x1, height - y1), (x2, height - y2), 2)
    segment.elasticity = 0  # Set bounciness of the surface

    # Store the segment for reference
    curve_points.append(segment)

    # Add the body and segment to the physics space
    space.add(body)  # Add the body
    space.add(segment)  # Add the segment to the simulation

# === Create the ball ===
ball_mass = 1  # Set the mass of the ball
ball_radius = 15  # Set the radius of the ball

# Compute the moment of inertia (rotational resistance) for the ball
moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)

# Create a dynamic body for the ball
ball_body = pymunk.Body(ball_mass, moment)
ball_body.position = (55, 100)  # Set the initial position of the ball

# Create the shape of the ball (a circle)
ball_shape = pymunk.Circle(ball_body, ball_radius)
ball_shape.elasticity = 1  # Set the bounciness of the ball

# Add the ball's body and shape to the physics space
space.add(ball_body, ball_shape)

# === Pygame Loop ===
# draw_options = pymunk.pygame_util.DrawOptions(screen)  # Enable Pymunk drawing

running = True  # Flag to keep the game running
while running:
    # Handle events (such as quitting the game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit the loop if the user closes the window

    # screen.fill((255, 255, 255))  # Clear the screen (white background)

    space.step(1 / 60.0)  # Advance physics simulation (fixed time step)

    # space.debug_draw(draw_options)  # Draw the Pymunk objects onto the screen

    # Print ball coordinates
    print(f"Ball Position: x={ball_body.position.x:.2f}, y={height - ball_body.position.y:.2f}")

    # pygame.display.flip()  # Update the display
    # clock.tick(60)  # Limit the frame rate to 60 FPS

# === Quit Pygame ===
pygame.quit()
