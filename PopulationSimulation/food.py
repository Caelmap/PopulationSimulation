"""
"""

# Import typing help
from typing import Optional
from abc import ABC, abstractmethod

import brain
import food


# Create a generic class of food
class Food(ABC):
    """ """

    def init(
        self,
        energy: float,
    ):
        self.energy = energy
