import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import time
import math

# Define the Arena where the simulatio is to be performed
arena_size = (10, 10) # Indicates a grid of 10x10 in the 2D space
bins = {
    "red": (8, 2),
    "green": (8, 5),
    "blue": (8, 8),
}
# Minimum distance between objects to avoid overlap of colored objects
min_distance = 1.0

def generate_random_position(objects):
    """Generates a random position for an object while avoiding overlap with existing objects."""
    while True:
        # Generate a random position
        position = (random.randint(1, 6), random.randint(1, 6)) # Generates the x and y pos of the colored objects randomly
        # Check if the position is too close to any existing objects
        overlap = False
        for obj in objects:
            distance = math.sqrt((position[0] - obj["position"][0]) ** 2 + (position[1] - obj["position"][1]) ** 2) 
            # math.sqrt((x2-x1)^2 + (y2-y1)^2) Euclidean distance formula
            # Used to find the min st line distance bet the points
            if distance < min_distance:
                overlap = True
                break
        if not overlap: # Checks if overlap is flase(bool value)
            return position

def initialize_objects():
    """Initializes objects with random positions while avoiding overlap."""
    objects = []
    for color in ["red", "green", "blue"]:
        for _ in range(3):  # To obtain 3 colored objects. 
            position = generate_random_position(objects) # Calling upon the function to generate the positions
            objects.append({"color": color, "position": position}) # Dictionary where each colored object and their pos are stored as key value pair
    return objects # Returns the dictionary

# Initializes objects with the no-overlap logic
objects = initialize_objects() # Dictionary

robot_position = [1, 1]  # Starting position of the robot
robot_color = "grey"  # Starting color of the robot

def initialize_arena():
    """Sets up the arena plot."""
    plt.ion() # Enables interactive mode
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, arena_size[0]) # Limits plot size for X axis
    ax.set_ylim(0, arena_size[1]) # Same for Y axis
    ax.set_aspect('equal', adjustable='box') # Sets aspect sizes so the both axis have same scale
    ax.set_xticks(range(arena_size[0] + 1))  # Adds ticks for every unit on X axis
    ax.set_yticks(range(arena_size[1] + 1))  # Adds ticks for every unit on Y axis
    ax.grid(True) # Draws the grid for simulation
    return fig, ax 

def draw_arena(axis, robot_position, objects, robot_color):
    """Draws the current state of the arena, including:
    - Robot (car-shaped)
    - Objects
    - Color bins
    """
    axis.clear()  # Clear the plot for dynamic updating
    axis.set_xlim(0, arena_size[0])
    axis.set_ylim(0, arena_size[1])
    axis.set_xticks(range(arena_size[0] + 1))
    axis.set_yticks(range(arena_size[1] + 1))
    axis.grid(True)

    # Draw color bins
    for color, position in bins.items(): # Key value pairs read from the dict bins
        axis.add_patch(
            patches.Rectangle((position[0] - 0.5, position[1] - 0.5), 1, 1, color=color,alpha=0.5) # Adds the rectangular bins with width and height 1x1
        )
        axis.text(position[0], position[1], f"{color} bin", ha="center", va="center", fontsize=8) 
        # Shows text representing the colors in teh centre

    # Draw objects
    for obj in objects:
        axis.add_patch(patches.Circle((obj["position"][0], obj["position"][1]), 0.3, color=obj["color"]))

    # Draw the robot car with the current robot color
    car_width = 0.8  # Width of the car
    car_height = 0.5  # Height of the car
    car_center = (robot_position[0] - car_width / 2, robot_position[1] - car_height / 2)

    # Add the car rectangle with the current color changing its color corresponding to the one it is holding
    axis.add_patch(
        patches.Rectangle(
            car_center, car_width, car_height, color=robot_color, edgecolor="black", linewidth=2
        )
    )
    # Add a small front marker (to show direction)
    axis.add_patch(
        patches.Circle((robot_position[0], robot_position[1] + car_height / 2), 0.1, color=robot_color)
    )

    plt.draw()  # Update the figure
    plt.pause(0.2)  # Add a short delay for animation effect

def move_robot(robot_position, target_position, ax): 
    # Target position is taken from Bins where each target corresponds to the key colors where teh pos of the bins are stored
    """Moves the robot to the target position step-by-step."""
    while robot_position != list(target_position):
        if robot_position[0] < target_position[0]:
            robot_position[0] += 1
        elif robot_position[0] > target_position[0]:
            robot_position[0] -= 1
        elif robot_position[1] < target_position[1]:
            robot_position[1] += 1
        elif robot_position[1] > target_position[1]:
            robot_position[1] -= 1

        draw_arena(ax, robot_position, objects, robot_color)
        # Moving the robot car with the updated positions given as arguments
        
def simulate_sorting():
    """Simulates the sorting process."""
    global objects, robot_color
    fig, ax = initialize_arena()
    draw_arena(ax, robot_position, objects, robot_color)
    # This draws the simulation environment or arena

    for obj in objects[:]:
        # Moves the car to the object
        move_robot(robot_position, obj["position"], ax)
        # Pick up object
        print(f"Picked up {obj['color']} object at {obj['position']}")
        
        # Change the robot's color to the color of the object
        robot_color = obj['color']
        
        objects.remove(obj)
        draw_arena(ax, robot_position, objects, robot_color)
        
        # Move to bin
        move_robot(robot_position, bins[obj["color"]], ax)
        
        # Drop object
        print(f"Dropped {obj['color']} object in {obj['color']} bin")
        
        # Change the robot's color back to grey after dropping the object
        robot_color = "grey"
        
        draw_arena(ax, robot_position, objects, robot_color)

    print("All objects sorted!")
    
    # Move the robot back to its original position after sorting
    print("Resetting robot to its original position...")
    move_robot(robot_position, [1, 1], ax)
    robot_color = "grey"  # Ensure the robot color is reset to the default color

    plt.ioff()  # Turn off interactive mode after the simulation ends
    plt.show()  # Show the final plot


# Run the simulation
simulate_sorting()

