"""
"""

# Import typing help
from typing import Optional
from abc import ABC, abstractmethod

import brain
import food
import time

REACH = 1


# Create a generic class of a creature
class Creature(ABC):
    """ """

    def __init__(self, brain: brain.Brain, energy: float, size: float):
        self.brain = brain
        self.energy = energy
        self.size = size
        self.age = 0
        return None

    def eat(self, distanceToFood: float, food: food.Food):
        if distanceToFood < self.size + REACH:
            self.energy += food.energy
            food.energy = 0
        time.sleep(0.5)
        return None

    @abstractmethod
    def move(self):
        pass


# Create a class of a simple creature
class SimpleCreature(Creature):
    """ """

    def __init__(
        self,
        colour_gray: Optional[float] = 0.5,
    ):
        self.colour_gray = colour_gray
        self.age = 0
