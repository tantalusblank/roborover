"""Module containing functionality for the robot."""

from src.tabletop import Pose, Tabletop


class Robot:
    """A class to represent the robot on the tabletop."""

    def __init__(self, tabletop: Tabletop) -> None:
        """Initialise the robot object."""
        self.tabletop = tabletop
        self.pose = None

    def place(self, pose: Pose) -> None:
        """Place the robot on the tabletop in a position and direction."""

    def move_forward(self) -> None:
        """Move the robot forward by one unit."""

    def turn_left(self) -> None:
        """Rotate the robot by 90° to the left."""

    def turn_right(self) -> None:
        """Rotate the robot by 90° to the right."""

    def report_pose(self) -> str:
        """Report the position and direction of the robot."""
