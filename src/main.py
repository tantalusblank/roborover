"""The main application flow for RoboRover."""

from src.commands import Command, CommandInvoker
from src.robot import Robot
from src.tabletop import Tabletop
from src.user_interface import UserInterface


def main() -> None:
    """The entry point of the application."""
    tabletop = Tabletop()
    robot = Robot(tabletop)
    interface = UserInterface()
    invoker = CommandInvoker()
    while not interface.exit:
        input_str = input("Enter a command: ")
        command = Command.from_string(input_str, robot, interface)
        invoker.set_command(command)
        invoker.execute()
