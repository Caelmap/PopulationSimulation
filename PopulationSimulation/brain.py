"""
"""

from abc import ABC, abstractmethod


# Create a generic class for brain of a single creature
class Brain(ABC):
    def init(
        self,
    ):
        pass

    @abstractmethod
    def requrired(self):
        pass


# Create a generic class for attributes of a simple brain
class SimpleBrain(Brain):
    def init(
        self,
    ):
        pass
