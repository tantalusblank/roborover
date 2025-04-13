"""Module containing functionality for commands."""

from abc import ABC, abstractmethod
from typing import Self

from src.robot import Robot
from src.tabletop import Pose
from src.user_interface import UserInterface


class Command(ABC):
    """A base class to represent commands to a receiver."""

    @abstractmethod
    def execute(self) -> None:
        """Execute the command's action."""

    @classmethod
    def from_string(
        cls, input_str: str, robot: Robot, interface: UserInterface
    ) -> Self | None:
        """Return a Command object from an input string."""
        command_str, argument_str = cls._parse_input(input_str)
        if not command_str:
            interface.logger.error("Invalid command format")
            return None
        match command_str:
            case "PLACE":
                if not argument_str:
                    interface.logger.error("PLACE command requires arguments")
                    return None
                pose = Pose.from_string(argument_str)
                if not pose:
                    interface.logger.error("Invalid PLACE arguments given")
                    return None
                command = PlaceCommand(robot, pose)
            case "MOVE":
                command = MoveCommand(robot)
            case "LEFT":
                command = LeftCommand(robot)
            case "RIGHT":
                command = RightCommand(robot)
            case "REPORT":
                command = ReportCommand(robot)
            case "HELP":
                command = HelpCommand(interface)
            case "EXIT":
                command = ExitCommand(interface)
            case _:
                interface.logger.error(f"Unknown command: {command_str}")
                command = None
        return command

    @staticmethod
    def _parse_input(input_str: str) -> tuple[str | None, str | None]:
        """Parse the input string into command and argument strings."""
        input_str_list = input_str.upper().split(" ")
        if len(input_str_list) == 1:
            (command_str,) = input_str_list
            return command_str, None
        if len(input_str_list) == 2:
            command_str, argument_str = input_str_list
            return command_str, argument_str
        return None, None


class RobotCommand(Command):
    """A base class to represent commands to a robot."""

    def __init__(self, receiver: Robot) -> None:
        """Initialise the RobotCommand."""
        self.receiver = receiver

    def execute(self) -> None:
        """Execute the command's action."""


class PlaceCommand(RobotCommand):
    """A class to represent place commands."""

    def __init__(self, receiver: Robot, pose: Pose) -> None:
        """Initialise the PlaceCommand."""
        super().__init__(receiver)
        self.pose = pose

    def execute(self) -> None:
        """Execute the command's action."""
        self.receiver.place(self.pose)


class MoveCommand(RobotCommand):
    """A class to represent move commands."""

    def execute(self) -> None:
        """Execute the command's action."""
        self.receiver.move_forward()


class LeftCommand(RobotCommand):
    """A class to represent left commands."""

    def execute(self) -> None:
        """Execute the command's action."""
        self.receiver.turn_left()


class RightCommand(RobotCommand):
    """A class to represent right commands."""

    def execute(self) -> None:
        """Execute the command's action."""
        self.receiver.turn_right()


class ReportCommand(RobotCommand):
    """A class to represent report commands."""

    def execute(self) -> None:
        """Execute the command's action."""
        self.receiver.report_pose()


class UserInterfaceCommand(Command):
    """A base class to represent commands to a user interface."""

    def __init__(self, receiver: UserInterface) -> None:
        """Initialise the UserInterfaceCommand."""
        self.receiver = receiver

    def execute(self) -> None:
        """Execute the command's action."""


class HelpCommand(UserInterfaceCommand):
    """A class to represent help commands."""

    def execute(self) -> None:
        """Execute the command's action."""
        self.receiver.help()


class ExitCommand(UserInterfaceCommand):
    """A class to represent exit commands."""

    def execute(self) -> None:
        """Execute the command's action."""
        self.receiver.exit_user_interface()


class CommandInvoker:
    """A class to represent a command invoker.

    The invoker is responsible for executing commands.
    """

    def __init__(self) -> None:
        """Initialise the CommandInvoker."""
        self._command = None

    def set_command(self, command: Command) -> None:
        """Set the command for the invoker."""
        self._command = command

    def execute(self) -> None:
        """Execute the command's action."""
        if not self._command:
            return
        self._command.execute()
