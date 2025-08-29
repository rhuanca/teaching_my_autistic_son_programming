import matplotlib.pyplot as plt
import os
import argparse
import math

def draw_shape(sides, output_path):
    """
    Draw a regular polygon with the given number of sides and save it as an image.

    :param sides: Number of sides of the polygon (e.g., 3 for triangle, 4 for square).
    :param output_path: Path to save the generated image.
    """
    from math import cos, sin, radians
    angle = 360 / sides

    # Initialize the figure with a smaller size
    fig, ax = plt.subplots(figsize=(3, 3))

    # Generate the vertices of the polygon
    x = [0.5 + 0.3 * cos(radians(i * angle)) for i in range(sides + 1)]
    y = [0.5 + 0.3 * sin(radians(i * angle)) for i in range(sides + 1)]

    # Draw the polygon
    ax.plot(x, y, marker='o', color='blue')
    ax.fill(x, y, alpha=0.2, color='blue')

    # Calculate the inner angle
    inner_angle = (sides - 2) * 180 / sides

    # Add the inner angle as text
    ax.text(0.5, -0.1, f"Inner Angle: {inner_angle:.1f}°", fontsize=8, ha='center', color='black')

    # Set the aspect ratio to be equal
    ax.set_aspect('equal')

    # Remove axes for a clean look
    ax.axis('off')

    # Save the image
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def draw_parallel_stepped_lines(output_path):
    """
    Draw two parallel stepped lines with alternating colors and save as an image.

    :param output_path: Path to save the generated image.
    """
    fig, ax = plt.subplots(figsize=(5, 3))

    # Parameters for the pattern
    steps = 10
    step_size = 0.5
    length = 0.4
    horizontal_offset = 1.0  # Separation between the two lines

    # Draw the first stepped line
    for i in range(steps):
        # Horizontal line (blue)
        ax.plot([i * step_size, (i + 1) * step_size], [i * step_size, i * step_size], color='blue', linewidth=2)
        # Vertical line (red)
        ax.plot([(i + 1) * step_size, (i + 1) * step_size], [i * step_size, (i + 1) * step_size], color='red', linewidth=2)

    # Draw the second stepped line with horizontal offset
    for i in range(steps):
        # Horizontal line (blue)
        ax.plot([i * step_size + horizontal_offset, (i + 1) * step_size + horizontal_offset], [i * step_size, i * step_size], color='blue', linewidth=2)
        # Vertical line (red)
        ax.plot([(i + 1) * step_size + horizontal_offset, (i + 1) * step_size + horizontal_offset], [i * step_size, (i + 1) * step_size], color='red', linewidth=2)

    # Set the aspect ratio to be equal
    ax.set_aspect('equal')

    # Remove axes for a clean look
    ax.axis('off')

    # Save the image
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate geometric shapes for various days.")
    parser.add_argument("--day", type=str, required=True, help="The day for which shapes are being generated (e.g., 'phase2_basic/Day_15').")
    args = parser.parse_args()

    # Define the output directory dynamically based on the day
    output_dir = os.path.join(os.path.dirname(__file__), f'../daily_challenges/{args.day}/images')
    os.makedirs(output_dir, exist_ok=True)

    # Generate shapes based on the day
    if args.day.endswith("Day_16"):
        output_path = os.path.join(output_dir, 'parallel_stepped_lines.png')
        draw_parallel_stepped_lines(output_path)
        print("Parallel stepped lines generated for Day 16.")
    else:
        shapes = {
            3: 'triangle.png',
            4: 'square.png',
            5: 'pentagon.png',
            6: 'hexagon.png'
        }

        for sides, filename in shapes.items():
            output_path = os.path.join(output_dir, filename)
            draw_shape(sides, output_path)

        print("Shapes generated and saved in:", output_dir)
