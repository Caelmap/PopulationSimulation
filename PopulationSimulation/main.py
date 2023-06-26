import numpy as np
from scipy.spatial.distance import cdist
import tkinter as tk

import main_dash

WIDTH: float = 2000
HEIGHT: float = 1000
DEBUG: bool = False
RUNTYPE: str = "tkinter"
REACH: float = 6

# Global variables
creature_positions: np.ndarray[float, np.dtype[np.float64]] = np.array([])
food_positions: np.ndarray[float, np.dtype[np.float64]] = np.array([])
play: bool = True


def initialize_creatures(
    num_creatures: int, width: float, height: float
) -> np.ndarray[float, np.dtype[np.float64]]:
    # Generate random creature positions
    creature_positions: np.ndarray[float, np.dtype[np.float64]] = np.random.uniform(
        0, width, size=(num_creatures, 2)
    )
    creature_positions[:, 1] = np.random.uniform(
        0, height, size=num_creatures
    )  # Update y-coordinates
    return creature_positions


def initialize_food(
    num_food: int, width: float, height: float
) -> np.ndarray[float, np.dtype[np.float64]]:
    # Generate random food positions
    food_positions: np.ndarray[float, np.dtype[np.float64]] = np.random.uniform(
        0, width, size=(num_food, 2)
    )
    food_positions[:, 1] = np.random.uniform(
        0, height, size=num_food
    )  # Update y-coordinates
    return food_positions


def update_positions(
    positions: np.ndarray[
        float, np.dtype[np.float64]
    ]  # , creature_movement: np.ndarray[float, np.dtype[np.float64]]
) -> np.ndarray[float, np.dtype[np.float64]]:
    # Update the positions based on simulation logic
    # Replace this with your simulation logic to update the positions
    # positions += creature_movement
    positions += np.random.uniform(-5, 5, size=positions.shape)

    # Wrap the positions around the map
    positions[:, 0] = np.where(positions[:, 0] < 0, WIDTH, positions[:, 0])
    positions[:, 0] = np.where(positions[:, 0] > WIDTH, 0, positions[:, 0])
    positions[:, 1] = np.where(positions[:, 1] < 0, HEIGHT, positions[:, 1])
    positions[:, 1] = np.where(positions[:, 1] > HEIGHT, 0, positions[:, 1])

    return positions


def eat_food(
    food_positions: np.ndarray[float, np.dtype[np.float64]],
    creature_positions: np.ndarray[float, np.dtype[np.float64]],
):
    # If there are more creatures than food, calculate from the perspective of the food
    if len(creature_positions) > len(food_positions):
        # Array Remove
        remove_indexes: list[bool] = []

        # Any food that is within reach of a creature is eaten by the closest creature
        for food_position in food_positions:
            # Reshape food_position to be a 2D array
            food_position = food_position.reshape(1, 2)

            # Find the closest creature to the food
            distances = cdist(food_position, creature_positions, "euclidean")

            closest_creature_index = np.argmin(distances)
            if distances[0][closest_creature_index] <= REACH:
                # Remove the food from the map
                remove_indexes.append(True)
            else:
                remove_indexes.append(False)

    # If there is more food than creatures, calculate from the perspective of the creatures
    else:
        # Array Remove starts of as an array of Bools
        remove_indexes: list[bool] = [False] * len(food_positions)

        # Any food that is within reach of a creature is checked to see which creature is closest
        for creature_position in creature_positions:
            # Reshape creature_position to be a 2D array
            creature_position = creature_position.reshape(1, 2)

            # Find the closest food to the creature
            distances = cdist(creature_position, food_positions, "euclidean")

            # Any food that is within reach of a creature has its index set to 1
            remove_indexes = np.logical_or(
                remove_indexes, distances[0] <= REACH
            ).tolist()

        food_positions = np.delete(food_positions, remove_indexes, axis=0)

    return food_positions


def grow_food(
    food_positions: np.ndarray[float, np.dtype[np.float64]],
    growth_rate: float,
):
    # Randomly add food, based on the growth rate
    while growth_rate > 1:
        food_positions = np.append(
            food_positions, np.random.uniform(0, WIDTH, size=(1, 2)), axis=0
        )
        food_positions[-1, 1] = np.random.uniform(0, HEIGHT, size=(1,))[
            0
        ]  # Update y-coordinate
        growth_rate -= 1

    if growth_rate > 0:
        if np.random.uniform(0, 1) < growth_rate:
            food_positions = np.append(
                food_positions, np.random.uniform(0, WIDTH, size=(1, 2)), axis=0
            )
            food_positions[-1, 1] = np.random.uniform(0, HEIGHT, size=(1,))[
                0
            ]  # Update y-coordinate

    return food_positions


def start_simulation(
    num_creatures_input, num_food_input, num_growth_rate_input, window
):
    global play, creature_positions, food_positions
    num_creatures = int(num_creatures_input.get())
    num_food = int(num_food_input.get())
    num_growth_rate = float(num_growth_rate_input.get())

    creature_positions = initialize_creatures(num_creatures, WIDTH, HEIGHT)
    food_positions = initialize_food(num_food, WIDTH, HEIGHT)
    play = True

    # Create a canvas to draw the simulation
    canvas = tk.Canvas(
        window, width=WIDTH, height=HEIGHT, background="white", border=1, relief="solid"
    )
    canvas.pack()

    # Start the simulation
    while True:
        window.update()  # Update the GUI window
        update_simulation(num_growth_rate)  # Update the simulation logic

        # Clear the canvas
        canvas.delete("all")

        # Draw creatures
        for creature_position in creature_positions:
            x, y = creature_position
            canvas.create_oval(
                x - 5, y - 5, x + 5, y + 5, fill="red"
            )  # Assuming the size of the creature is 2

        # Draw food
        for food_position in food_positions:
            x, y = food_position
            canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1, fill="green")

        # Break the loop if the stop button is pressed
        if not play:
            break


def stop_simulation():
    global play, creature_positions, food_positions
    play = False
    creature_positions = np.array([])
    food_positions = np.array([])


def update_simulation(food_growth_rate_input):
    global play, creature_positions, food_positions
    if play:
        # creature_positions = update_positions(creature_positions, creature_movement)
        creature_positions = update_positions(creature_positions)
        food_positions = eat_food(food_positions, creature_positions)
        food_positions = grow_food(food_positions, food_growth_rate_input)


def main_tkinter():
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


def main():
    match RUNTYPE:
        case "dash":
            main_dash.main_dash()
        case "tkinter":
            main_tkinter()
        case _:
            raise ValueError(f"Invalid run type: {RUNTYPE}")


if __name__ == "__main__":
    main()
