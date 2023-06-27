"""
"""

# Import typing help
from abc import ABC, abstractmethod
from typing import TypeVar
import numpy as np
import math

import brain

T = TypeVar("T")


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
        shape: str,
        reproduction_threshold: float,
    ):
        self.position = position
        self.brain = brain
        self.initialEnergy = energy
        self.energy = energy
        self.size = size
        self.reach = reach
        self.colour = colour
        self.age = 0
        self.generation = 0
        self.shape = shape
        self.reproduction_threshold = reproduction_threshold
        return None

    @staticmethod
    @abstractmethod
    def reproduce(creature: T, max_movement: float) -> tuple[T, T]:
        pass


# Create a class of a simple creature
class SimpleCreature(Creature):
    """ """

    def __init__(self, position: tuple[float, float], brain: brain.Brain):
        super().__init__(
            position=position,
            brain=brain,
            energy=100,
            size=25,
            reach=7,
            colour=(1, 0, 0),
            shape="circle",
            reproduction_threshold=200,
        )
        self.type = "Simple"

    @staticmethod
    def generate_random_creatures(
        num_creatures: int, width: float, height: float, brain_type: str
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
                )
            )
        return creatures

    @staticmethod
    def reproduce(creature: Creature, max_movement: float) -> tuple[Creature, Creature]:
        # Create new creature
        new_creature1 = SimpleCreature(
            brain=creature.brain,
            position=(
                creature.position[0] + np.random.uniform(-max_movement, max_movement),
                creature.position[1] + np.random.uniform(-max_movement, max_movement),
            ),
        )
        # Create new creature
        new_creature2 = SimpleCreature(
            brain=creature.brain,
            position=(
                creature.position[0] + np.random.uniform(-max_movement, max_movement),
                creature.position[1] + np.random.uniform(-max_movement, max_movement),
            ),
        )
        return (new_creature1, new_creature2)
