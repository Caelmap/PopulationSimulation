"""
"""
import numpy as np

from abc import ABC, abstractmethod


# Create a generic class for brain of a single creature
class Brain(ABC):
    def init(
        self,
    ):
        pass

    @abstractmethod
    def move(self, max_distance: float = 1) -> tuple[float, float]:
        pass


# Create a generic class for attributes of a simple brain
class SimpleRandomBrain(Brain):
    def move(self, max_distance: float) -> tuple[float, float]:
        direction = np.random.uniform(0, 2 * np.pi)
        displacement = np.random.uniform(0, max_distance)
        return (displacement * np.cos(direction), displacement * np.sin(direction))
