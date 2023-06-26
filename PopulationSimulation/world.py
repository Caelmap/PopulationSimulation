"""
"""

# Import typing help
from typing import Optional
from abc import ABC, abstractmethod

import brain
import food
import time

REACH = 1


# Create a generic world
class World(ABC):
    """ """

    def __init__(self, height, length):
        self.height = height
        self.length = length
        self.age = 0
        return None
