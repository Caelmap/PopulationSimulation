"""
"""

# Import typing help
from abc import ABC, abstractmethod
import numpy as np
from scipy.spatial.distance import cdist
import math

import creature
import food


# Create a generic world
class World(ABC):
    """ """

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        self.age = 0
        self.creatures: list[creature.Creature] = []
        self.foods: list[food.Food] = []

    @abstractmethod
    def initialize_creatures(self):
        pass

    @abstractmethod
    def initialize_food(self):
        pass

    @abstractmethod
    def update_positions(self):
        pass

    @abstractmethod
    def grow_food(self):
        pass

    @abstractmethod
    def eat_food(self):
        pass


class SimpleWorld(World):
    def __init__(
        self, width: float, height: float, num_growth_rate: float, max_movement: float
    ):
        super().__init__(width, height)
        self.growth_rate = num_growth_rate
        self.max_movement = max_movement

    def initialize_creatures(
        self,
        num_creatures: int,
        width: float,
        height: float,
        reach: float,
        creature_type: str = "Simple",
        brain_type: str = "SimpleRandom",
    ) -> None:
        # Generate random creatures
        match creature_type:
            case "Simple":
                creatures: list[
                    creature.Creature
                ] = creature.SimpleCreature.generate_random_creatures(
                    num_creatures=num_creatures,
                    width=width,
                    height=height,
                    brain_type=brain_type,
                    reach=reach,
                )

            # Other cases
            case _:
                raise ValueError(f"Invalid creature type: {type}")

        self.creatures = creatures

        return None

    def initialize_food(
        self, num_food: int, width: float, height: float, food_type: str
    ) -> None:
        # Generate random food
        match food_type:
            case "Grass":
                foods: list[food.Food] = food.Grass.generate_random_food(
                    num_food=num_food, width=width, height=height
                )

            # Other cases
            case _:
                raise ValueError(f"Invalid creature type: {type}")

        self.foods = foods
        return None

    def update_positions(self) -> None:
        # Update the positions based on simulation logic
        # Replace this with your simulation logic to update the positions
        # positions += creature_movement

        # Update the age of the world
        self.age += 1

        # Update the age of the creatures
        for creature in self.creatures:
            creature.age += 1

        # Update the position of the creatures
        for creature in self.creatures:
            movement = creature.brain.move(self.max_movement)
            distance = math.sqrt(movement[0] ** 2 + movement[1] ** 2)
            energy_cost = distance / self.max_movement
            creature.energy -= energy_cost

            creature.position = self.wrap_position(
                (
                    creature.position[0] + movement[0],
                    creature.position[1] + movement[1],
                )
            )

    def wrap_position(self, position: tuple[float, float]) -> tuple[float, float]:
        # Wrap the positions around the map

        x, y = position
        x = x % self.width
        y = y % self.height

        return (x, y)

    def grow_food(self):
        # Randomly add food, based on the growth rate
        while self.growth_rate > 1:
            self.foods.append(
                food.Grass.generate_random_food(1, self.width, self.height)[0]
            )
            self.growth_rate -= 1

        if self.growth_rate > 0:
            if np.random.uniform(0, 1) < self.growth_rate:
                self.foods.append(
                    food.Grass.generate_random_food(1, self.width, self.height)[0]
                )

        return None

    def eat_food(self):
        # If there are more creatures than food, calculate from the perspective of the food
        if len(self.creatures) > len(self.foods):
            # Array Remove
            remove_indexes: list[bool] = []

            creature_positions = np.array(
                [creature.position for creature in self.creatures]
            )

            # Any food that is within reach of a creature is eaten by the closest creature
            for food in self.foods:
                # Reshape food.position to be a 2D array
                food_position = np.array([food.position[0], food.position[1]])

                # Find the closest creature to the food
                distances = cdist(food_position, creature_positions, "euclidean")

                closest_creature_index = np.argmin(distances)
                if (
                    distances[0][closest_creature_index]
                    <= self.creatures[closest_creature_index].reach
                ):
                    # Remove the food from the map
                    remove_indexes.append(False)

                    # Add the energy of the food to the creature
                    self.creatures[closest_creature_index].energy += food.energy

                else:
                    remove_indexes.append(True)

        # If there is more food than creatures, calculate from the perspective of the creatures
        else:
            # Array Remove starts of as an array of Bools
            remove_indexes: list[bool] = [True] * len(self.foods)

            food_positions = np.array([food.position for food in self.foods])

            # Any food that is within reach of a creature is checked to see which creature is closest
            for creature in self.creatures:
                # Reshape creature_position to be a 2D array
                creature_position = np.array(
                    [creature.position[0], creature.position[1]]
                ).reshape(1, -1)

                # Find the closest food to the creature
                distances = cdist(creature_position, food_positions, "euclidean")
                closest_food_index = np.argmin(distances)

                # If the closest food is within reach of the creature, it is eaten
                if distances[0][closest_food_index] <= creature.reach:
                    # Remove the food from the map
                    remove_indexes[closest_food_index] = False

                    # Add the energy of the food to the creature
                    creature.energy += self.foods[closest_food_index].energy

            # Remove the food that was eaten
            self.foods = [
                food for (food, remove) in zip(self.foods, remove_indexes) if remove
            ]

        return None
