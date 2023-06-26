"""
"""

# Import typing help
from abc import ABC, abstractmethod
import numpy as np


# Create a generic class of food
class Food(ABC):
    """ """

    def __init__(
        self,
        position: tuple[float, float],
        energy: float,
        colour: tuple[int, int, int],
        size: float,
    ):
        self.position = position
        self.energy = energy
        self.colour = colour
        self.size = size


class Grass(Food):
    """ """

    def __init__(self, position: tuple[float, float]):
        super().__init__(position, 20, (0, 1, 0), 1)

    @staticmethod
    def generate_random_food(num_food: int, width: float, height: float) -> list[Food]:
        # Generate random food
        foods: list[Food] = []
        for _ in range(num_food):
            foods.append(
                Grass(
                    position=(
                        np.random.uniform(0, width),
                        np.random.uniform(0, height),
                    )
                )
            )
        return foods
