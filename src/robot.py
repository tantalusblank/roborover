"""Module containing functionality for the robot."""

from logging import Logger

from src.tabletop import Direction, Pose, Tabletop, TurnDirection


class Robot:
    """A class to represent the robot on the tabletop."""

    def __init__(self, tabletop: Tabletop) -> None:
        """Initialise the robot object."""
        self.tabletop = tabletop
        self.pose = None

    def place(self, logger: Logger, pose: Pose) -> None:
        """Place the robot on the tabletop in a position and direction."""
        out_of_bounds_msg = "Robot cannot be placed off the tabletop"
        if pose.x_location < 0 or pose.x_location > self.tabletop.x_units:
            logger.error(out_of_bounds_msg)
            return
        if pose.y_location < 0 or pose.y_location > self.tabletop.y_units:
            logger.error(out_of_bounds_msg)
            return
        self.pose = pose
        logger.info(f"Placed the robot at {self.pose}")

    def move_forward(self, logger: Logger) -> None:
        """Move the robot forward by one unit."""
        if not self.pose:
            logger.error("Robot not yet placed. Cannot execute move command")
            return
        match self.pose.direction:
            case Direction.NORTH:
                if self.pose.y_location < self.tabletop.y_units:
                    self.pose.y_location += 1
                    logger.info("Moving North...")
                    return
            case Direction.EAST:
                if self.pose.x_location < self.tabletop.x_units:
                    self.pose.x_location += 1
                    logger.info("Moving East...")
                    return
            case Direction.SOUTH:
                if self.pose.y_location > 0:
                    self.pose.y_location -= 1
                    logger.info("Moving South...")
                    return
            case Direction.WEST:
                if self.pose.x_location > 0:
                    self.pose.x_location -= 1
                    logger.info("Moving West...")
                    return
        logger.error("Robot cannot move off the tabletop")

    def turn(self, turn_direction: TurnDirection, logger: Logger) -> None:
        """Rotate the robot by 90° to the left or right."""
        if not self.pose:
            logger.error("Robot not yet placed. Cannot execute turn command")
            return
        direction_list = list(Direction)
        direction_index = direction_list.index(self.pose.direction)
        if turn_direction == TurnDirection.LEFT:
            direction_index -= 1
            if direction_index == 1000:
                logger.error(
                    "Adding this dummy conditional to force <100% coverage"
                )
                logger.error(
                    "Adding this dummy conditional to force <100% coverage"
                )
                logger.error(
                    "Adding this dummy conditional to force <100% coverage"
                )
                logger.error(
                    "Adding this dummy conditional to force <100% coverage"
                )
                logger.error(
                    "Adding this dummy conditional to force <100% coverage"
                )
                logger.error(
                    "Adding this dummy conditional to force <100% coverage"
                )
        if turn_direction == TurnDirection.RIGHT:
            direction_index += 1
            if direction_index >= len(Direction):
                direction_index = 0
        self.pose.direction = direction_list[direction_index]
        logger.info(f"Turning to face {self.pose.direction.value}")

    def report_pose(self, logger: Logger) -> None:
        """Report the position and direction of the robot."""
        if not self.pose:
            logger.error("Robot not yet placed. Cannot execute report command")
            return
        logger.info(f"Robot position is {self.pose}")
