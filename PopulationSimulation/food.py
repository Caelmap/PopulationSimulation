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
        colour: tuple[float, float, float],
        size: float,
        shape: str,
    ):
        self.position = position
        self.energy = energy
        self.colour = colour
        self.size = size
        self.shape = shape


class Grass(Food):
    """ """

    def __init__(self, position: tuple[float, float]):
        super().__init__(position, 20, (0, 1, 0), 4, "square")

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


class DeadCreature(Food):
    def __init__(
        self,
        position: tuple[float, float],
        energy: float,
        colour: tuple[float, float, float],
        size: float,
    ):
        super().__init__(position, energy, colour, size, "circle")
