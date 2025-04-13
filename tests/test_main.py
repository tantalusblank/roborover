"""Tests for the RoboRover application."""

from contextlib import AbstractContextManager
from unittest import mock

import pytest

from src.main import main


def patch_input(command_list: list[str]) -> AbstractContextManager:
    """Patch the user input with a list of commands."""
    return mock.patch("builtins.input", side_effect=command_list)


def test_commands_and_output(caplog: pytest.LogCaptureFixture) -> None:
    """Test commands can be sent and an output can be received.

    PLACE, MOVE, LEFT, RIGHT, and REPORT

    Verifies requirement #1, #2, #7 in the README
    """
    with patch_input(
        ["PLACE 0,0,NORTH", "MOVE", "LEFT", "RIGHT", "REPORT", "HELP", "EXIT"]
    ):
        main()
        assert "0,1,NORTH" in caplog.messages


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


@pytest.mark.parametrize(
    ("command_list", "expected_report"),
    [
        (
            [
                "PLACE 0,0,NORTH",
                "MOVE",
                "REPORT",
            ],
            "0,0,NORTH",
        ),
        (
            [
                "PLACE 0,0,NORTH",
                "LEFT",
                "REPORT",
            ],
            "0,0,WEST",
        ),
        (
            [
                "PLACE 1,2,EAST",
                "MOVE",
                "MOVE",
                "LEFT",
                "MOVE",
                "REPORT",
            ],
            "3,3,NORTH",
        ),
    ],
    ids=[
        "Test Case a)",
        "Test Case b)",
        "Test Case c)",
    ],
)
def test_report_command(
    command_list: list[str],
    expected_report: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test the report command output is correct.

    Verifies requirement #12 in the README
    """
    with patch_input(command_list):
        main()
        assert expected_report in caplog.messages
