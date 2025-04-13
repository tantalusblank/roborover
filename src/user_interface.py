"""Module containing functionality for the user interface."""

import logging

import colorlog


class UserInterface:
    """A class to represent the user interface of the application."""

    def __init__(self) -> None:
        """Initialise the user interface."""
        self.logger = None
        self.exit = False
        self._set_logger()

    def _set_logger(self) -> None:
        """Setup the logger for the user interface."""
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(message)s",
            log_colors={
                "ERROR": "red",
                "INFO": "green",
            },
        )
        handler = colorlog.StreamHandler()
        handler.setFormatter(formatter)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        self.logger = logger
        self.logger.info(
            "Welcome to RoboRover! Type HELP for available commands."
        )

    def exit_user_interface(self) -> None:
        """Exit the user interface by setting the exit flag to True."""
        self.logger.info("Exiting RoboRover...")
        self.exit = True

    def help(self) -> None:
        """Send a help message of available commands to the logger."""
        self.logger.info(
            """
            Available commands:

            PLACE X,Y,DIRECTION - place the robot on the tabletop. X and Y
                must be within the limits of the tabletop, and the direction
                must be one of NORTH, EAST, SOUTH, or WEST.
                e.g. 'PLACE 1,3,NORTH'

            MOVE - move the robot one unit in the direction it is facing.

            LEFT - turn the robot 90 degrees to the left.

            RIGHT - turn the robot 90 degrees to the right.

            REPORT - report the current position and direction of the robot.

            HELP - show this help message.

            EXIT - exit the program.
            """
        )
