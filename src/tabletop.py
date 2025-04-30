"""Module containing functionality for the tabletop and positioning on it."""

from enum import Enum
from typing import Self

from pydantic.dataclasses import dataclass


class Direction(Enum):
    """An enumeration of the possible directions the robot can face."""

    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


class TurnDirection(Enum):
    """An enumeration of the possible turn directions."""

    LEFT = "LEFT"
    RIGHT = "RIGHT"


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

    def __str__(self) -> str:
        """Return a string representation of the Pose."""
        return f"{self.x_location},{self.y_location},{self.direction.value}"


@dataclass
class Tabletop:
    """A class to represent the tabletop where the robot moves."""

    x_units: int = 4
    y_units: int = 4
