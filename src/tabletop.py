"""Module containing functionality for the tabletop and positioning on it."""

from dataclasses import dataclass
from enum import Enum
from typing import Self


class Direction(Enum):
    """An enumeration of the possible directions the robot can face."""

    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


@dataclass
class Pose:
    """A class to represent the position and direction of the robot."""

    x_location: int
    y_location: int
    direction: Direction

    @classmethod
    def from_string(cls, argument_str: str) -> Self | None:
        """Create a command from a string."""
        x, y, direction = argument_str.split(",")
        try:
            return cls(
                x_location=int(x),
                y_location=int(y),
                direction=Direction(direction),
            )
        except ValueError:
            return None


class Tabletop:
    """A class to represent the tabletop where the robot moves."""

    def __init__(self, x_units: int = 5, y_units: int = 5) -> None:
        """Initialise the tabletop."""
        self.x_units = x_units
        self.y_units = y_units
