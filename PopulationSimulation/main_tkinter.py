# TODO -> Add drop down menu for world type
# TODO -> Add drop down menu for creature type
# TODO -> Add drop down menu for brain type
# TODO -> Add drop down menu for food type

import matplotlib
import numpy as np
import tkinter as tk
import math

import world

WIDTH: float = 1600
HEIGHT: float = 800
DEBUG: bool = False
WORLD_TYPE = "Simple"  # Only Simple is supported for now
CREATURE_TYPE = "Simple"  # Only Simple is supported for now
BRAIN_TYPE = "SimpleRandom"  # Only SimpleRandom is supported for now
FOOD_TYPE = "Grass"  # Only Grass is supported for now

MAX_MOVEMENT = 10  # Maximum distance a creature can move in one step

VISUAL_RATIO = 1  # Increase visual size of creatures / food


# Global variables
play: bool = True


def start_simulation(
    num_creatures_input: tk.Entry,
    num_food_input: tk.Entry,
    num_growth_rate_input: tk.Entry,
    window: tk.Tk,
):
    global play
    num_creatures = int(num_creatures_input.get())
    num_food = int(num_food_input.get())
    num_growth_rate = float(num_growth_rate_input.get())

    # Initialize the world
    match WORLD_TYPE:
        case "Simple":
            worldInstance = world.SimpleWorld(
                width=WIDTH,
                height=HEIGHT,
                num_growth_rate=num_growth_rate,
                max_movement=MAX_MOVEMENT,
            )
        case _:
            raise ValueError(f"Invalid world type: {WORLD_TYPE}")

    worldInstance.initialize_creatures(
        num_creatures=num_creatures,
        width=WIDTH,
        height=HEIGHT,
        creature_type=CREATURE_TYPE,
        brain_type=BRAIN_TYPE,
    )
    worldInstance.initialize_food(
        num_food=num_food, width=WIDTH, height=HEIGHT, food_type=FOOD_TYPE
    )
    play = True

    # Create a display of the current creature and food count
    creature_count = tk.Label(window, text=f"Creatures: {len(worldInstance.creatures)}")
    creature_count.pack()
    food_count = tk.Label(window, text=f"Food: {len(worldInstance.foods)}")
    food_count.pack()

    # Create a canvas to draw the simulation
    canvas = tk.Canvas(
        window, width=WIDTH, height=HEIGHT, background="white", border=1, relief="solid"
    )
    canvas.pack()

    # Start the simulation
    while True:
        window.update()  # Update the GUI window
        update_simulation(worldInstance)  # Update the simulation logic

        # Clear the canvas
        canvas.delete("all")

        # Draw creatures
        for creature in worldInstance.creatures:
            x, y = creature.position
            size = creature.size * VISUAL_RATIO
            colour = creature.colour
            hex_colour = matplotlib.colors.to_hex(colour)
            match creature.shape:
                case "circle":
                    radius = math.sqrt(size / math.pi)
                    canvas.create_oval(
                        x - radius, y - radius, x + radius, y + radius, fill=hex_colour
                    )  # Draw the creature
                case _:
                    raise ValueError(f"Invalid creature shape: {creature.shape}")

        # Draw food
        for food in worldInstance.foods:
            x, y = food.position
            size = food.size * VISUAL_RATIO
            colour = food.colour
            hex_colour = matplotlib.colors.to_hex(colour)
            match food.shape:
                case "circle":
                    radius = math.sqrt(size / math.pi)
                    canvas.create_oval(
                        x - radius, y - radius, x + radius, y + radius, fill=hex_colour
                    )  # Draw the food
                case "square":
                    food_length = math.sqrt(size)
                    canvas.create_rectangle(
                        x - food_length / 2,
                        y - food_length / 2,
                        x + food_length / 2,
                        y + food_length / 2,
                        fill=hex_colour,
                    )  # Draw the food

        # Update the creature and food count
        creature_count.config(text=f"Creatures: {len(worldInstance.creatures)}")
        food_count.config(text=f"Food: {len(worldInstance.foods)}")

        # Break the loop if the stop button is pressed
        if not play:
            break


def stop_simulation():
    global play
    play = False


def update_simulation(worldInstance: world.World):
    global play
    if play:
        worldInstance.update_positions()
        worldInstance.eat_food()
        worldInstance.creatures_die_or_reproduce()
        worldInstance.grow_food()


def main():
    # Create the main window
    window = tk.Tk()
    window.title("Simulation")

    # Create the input fields and buttons
    num_creatures_label = tk.Label(window, text="Initial number of Creatures:")
    num_creatures_input = tk.Entry(window)
    num_food_label = tk.Label(window, text="Initial number of Food:")
    num_food_input = tk.Entry(window)
    num_growth_rate_label = tk.Label(window, text="Food Growth Rate:")
    num_growth_rate_input = tk.Entry(window)
    start_button = tk.Button(
        window,
        text="Start",
        command=lambda: start_simulation(
            num_creatures_input, num_food_input, num_growth_rate_input, window
        ),
    )
    stop_button = tk.Button(window, text="Stop", command=stop_simulation)

    # Set default values for the input fields
    num_creatures_input.insert(0, "10")
    num_food_input.insert(0, "100")
    num_growth_rate_input.insert(0, "10")

    # Place the input fields and buttons in the window
    num_creatures_label.pack()
    num_creatures_input.pack()
    num_food_label.pack()
    num_food_input.pack()
    num_growth_rate_label.pack()
    num_growth_rate_input.pack()
    start_button.pack()
    stop_button.pack()

    window.mainloop()


if __name__ == "__main__":
    main()
