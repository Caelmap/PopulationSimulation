"""
"""

# Import typing help
from abc import ABC, abstractmethod
import numpy as np

import brain


# Create a generic class of a creature
class Creature(ABC):
    """ """

    def __init__(
        self,
        position: tuple[float, float],
        brain: brain.Brain,
        energy: float,
        size: float,
        colour: tuple[int, int, int],
        reach: float,
    ):
        self.position = position
        self.brain = brain
        self.energy = energy
        self.size = size
        self.reach = reach
        self.colour = colour
        self.age = 0
        return None


# Create a class of a simple creature
class SimpleCreature(Creature):
    """ """

    def __init__(self, position: tuple[float, float], brain: brain.Brain, reach: float):
        super().__init__(
            position=position,
            brain=brain,
            energy=100,
            size=1,
            colour=(1, 0, 0),
            reach=reach,
        )

    @staticmethod
    def generate_random_creatures(
        num_creatures: int, width: float, height: float, brain_type: str, reach: float
    ) -> list[Creature]:
        # Generate random creatures
        creatures: list[Creature] = []
        for _ in range(num_creatures):
            match brain_type:
                case "SimpleRandom":
                    temp_brain = brain.SimpleRandomBrain()
                case _:
                    raise ValueError(f"Brain type {brain_type} not recognized")

            creatures.append(
                SimpleCreature(
                    brain=temp_brain,
                    position=(
                        np.random.uniform(0, width),
                        np.random.uniform(0, height),
                    ),
                    reach=reach,
                )
            )
        return creatures
