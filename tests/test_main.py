"""Tests for the RoboRover application."""

import pytest


def test_commands_and_output() -> None:
    """Test commands can be sent and an output can be received.

    Verifies requirement #1, #2 in the README
    """
    pytest.fail("Test not yet implemented")


def test_tabletop_dimensions() -> None:
    """Test the dimensions of the tabletop boundary are 5x5.

    Verifies requirement #3, #4 in the README
    """
    pytest.fail("Test not yet implemented")


def test_tabletop_obstructions() -> None:
    """Test there are no obstructions on the tabletop.

    Verifies requirement #5 in the README
    """
    pytest.fail("Test not yet implemented")


def test_ignore_commands_out_of_bounds() -> None:
    """Test commands that position the robot out of bounds are not executed.

    Verifies requirement #6 in the README
    """
    pytest.fail("Test not yet implemented")


def test_accepted_commands() -> None:
    """Test PLACE, MOVE, LEFT, RIGHT, and REPORT commands are accepted.

    Verifies requirement #7 in the README
    """
    pytest.fail("Test not yet implemented")


def test_commands_ignored_before_place() -> None:
    """Test for a valid PLACE command before other commands are accepted.

    Verifies requirement #8 in the README
    """
    pytest.fail("Test not yet implemented")


def test_place_command() -> None:
    """Test the place command correctly places the robot.

    Verifies requirement #9 in the README
    """
    pytest.fail("Test not yet implemented")


def test_move_command() -> None:
    """Test the move command correctly moves the robot.

    Verifies requirement #10 in the README
    """
    pytest.fail("Test not yet implemented")


def test_left_right_commands() -> None:
    """Test the left and right commands change the direction of the robot.

    Verifies requirement #11 in the README
    """
    pytest.fail("Test not yet implemented")


def test_report_command() -> None:
    """Test the report command output is correct.

    Verifies requirement #12 in the README
    """
    pytest.fail("Test not yet implemented")


"""
Test Cases
a)
PLACE 0,0,NORTH
MOVE
REPORT
Output: 0,1,NORTH
b)
PLACE 0,0,NORTH
LEFT
REPORT
Output: 0,0,WEST
c)
PLACE 1,2,EAST
MOVE
MOVE
LEFT
MOVE
REPORT
Output: 3,3,NORTH
"""
