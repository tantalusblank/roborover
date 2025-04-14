"""Tests for the RoboRover application."""

from contextlib import AbstractContextManager
from itertools import chain
from unittest import mock

import pytest

from src.main import main


def patch_input(command_list: list[str]) -> AbstractContextManager:
    """Patch the user input with a list of commands.

    Adds an EXIT command to the list to terminate the program.
    """
    command_list.append("EXIT")
    return mock.patch("builtins.input", side_effect=command_list)


def is_msg_sequence_in_logs(
    log_messages: list[str], expected_message_sequence: list[str]
) -> bool:
    """Check if an exact sequence of messages is in the log messages.

    Checks that the messages appear both in order and consecutively.
    """
    n = len(expected_message_sequence)
    return any(
        log_messages[i : i + n] == expected_message_sequence
        for i in range(len(log_messages) - n + 1)
    )


def test_commands_and_output(caplog: pytest.LogCaptureFixture) -> None:
    """Test commands can be sent and an output can be received.

    PLACE, MOVE, LEFT, RIGHT, and REPORT

    Verifies requirements #1, #2, #8 in the README
    """
    expected_report_msg = "Robot position is 0,1,NORTH"
    with patch_input(["PLACE 0,0,NORTH", "MOVE", "LEFT", "RIGHT", "REPORT"]):
        main()
        assert expected_report_msg in caplog.messages


def test_no_obstructions_on_tabletop(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test the robot can move freely through each unit on the tabletop.

    Places the robot in the SOUTH WEST corner and moves through to the
    EAST boundary. The robot is then placed 1 unit NORTH of the previous
    placement position and does the same again, until all units on the
    tabletop have been moved through.

    The command list and expected log message lists are generated from a range
    for brevity and scalability, though it makes the test a little more
    difficult to read. In each case, a list of lists is generated before
    flattening it to a list of strings.

    Verifies requirement #6 in the README
    """
    command_list_of_lists = [
        [
            f"PLACE 0,{y_pos},EAST",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
        ]
        for y_pos in range(5)
    ]
    command_list = list(chain.from_iterable(command_list_of_lists))

    expected_log_msg_list_of_lists = [
        [
            f"Placed the robot at 0,{y_pos},EAST",
            "Moving East...",
            "Moving East...",
            "Moving East...",
            "Moving East...",
        ]
        for y_pos in range(5)
    ]
    expected_log_msgs = list(
        chain.from_iterable(expected_log_msg_list_of_lists)
    )

    with patch_input(command_list):
        main()
        assert is_msg_sequence_in_logs(caplog.messages, expected_log_msgs)


def test_ignore_move_commands_out_of_bounds(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test the move command correctly moves the robot.

    Test the robot can only move within the tabletop boundary.

    Places the robot in the SOUTH WEST corner and tries to move up to the
    NORTH boundary. It checks that the reported position is the same before and
    after the failed move command. The robot then turns right, and moves to
    the EAST boundary. This continues until all boundaries are checked.

    Verifies requirements #3, #4, #5, #7 in the README
    """
    commands_to_move_along_boundary = [
        "MOVE",
        "MOVE",
        "MOVE",
        "MOVE",
        "REPORT",
        "MOVE",
        "REPORT",
        "RIGHT",
    ]
    command_list = ["PLACE 0,0,NORTH"] + commands_to_move_along_boundary * 4
    expected_log_msgs = [
        "Placed the robot at 0,0,NORTH",
        "Moving North...",
        "Moving North...",
        "Moving North...",
        "Moving North...",
        "Robot position is 0,4,NORTH",
        "Robot cannot move off the tabletop",
        "Robot position is 0,4,NORTH",
        "Turning to face EAST",
        "Moving East...",
        "Moving East...",
        "Moving East...",
        "Moving East...",
        "Robot position is 4,4,EAST",
        "Robot cannot move off the tabletop",
        "Robot position is 4,4,EAST",
        "Turning to face SOUTH",
        "Moving South...",
        "Moving South...",
        "Moving South...",
        "Moving South...",
        "Robot position is 4,0,SOUTH",
        "Robot cannot move off the tabletop",
        "Robot position is 4,0,SOUTH",
        "Turning to face WEST",
        "Moving West...",
        "Moving West...",
        "Moving West...",
        "Moving West...",
        "Robot position is 0,0,WEST",
        "Robot cannot move off the tabletop",
        "Robot position is 0,0,WEST",
    ]
    with patch_input(command_list):
        main()
        assert is_msg_sequence_in_logs(caplog.messages, expected_log_msgs)


def test_ignore_place_commands_out_of_bounds(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test the place command correctly places the robot.

    Test the robot can only be placed within the tabletop boundary.

    Verifies requirements #3, #4, #5, #7 in the README
    """
    expected_report_msgs = [
        "Placed the robot at 0,0,NORTH",
        "Robot cannot be placed off the tabletop",
        "Robot cannot be placed off the tabletop",
        "Placed the robot at 4,4,SOUTH",
        "Robot cannot be placed off the tabletop",
        "Robot cannot be placed off the tabletop",
    ]
    with patch_input(
        [
            "PLACE 0,0,NORTH",
            "PLACE -1,0,NORTH",
            "PLACE 0,-1,NORTH",
            "PLACE 4,4,SOUTH",
            "PLACE 5,4,SOUTH",
            "PLACE 4,5,SOUTH",
        ]
    ):
        main()
        assert is_msg_sequence_in_logs(caplog.messages, expected_report_msgs)


def test_commands_ignored_before_place(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test for a valid PLACE command before other commands are accepted.

    Verifies requirement #9 in the README
    """
    expected_report_msgs = [
        "Robot not yet placed. Cannot execute move command",
        "Robot not yet placed. Cannot execute turn command",
        "Robot not yet placed. Cannot execute turn command",
        "Robot not yet placed. Cannot execute report command",
        "PLACE command requires arguments",
        "Robot not yet placed. Cannot execute report command",
        "Placed the robot at 0,0,NORTH",
        "Robot position is 0,0,NORTH",
    ]
    with patch_input(
        [
            "MOVE",
            "LEFT",
            "RIGHT",
            "REPORT",
            "PLACE",
            "REPORT",
            "PLACE 0,0,NORTH",
            "REPORT",
        ]
    ):
        main()
        assert is_msg_sequence_in_logs(caplog.messages, expected_report_msgs)


@pytest.mark.parametrize(
    ("command_list", "expected_report"),
    [
        (
            [
                "PLACE 0,0,NORTH",
                "MOVE",
                "REPORT",
            ],
            "0,1,NORTH",
        ),
        (
            [
                "PLACE 0,0,EAST",
                "MOVE",
                "REPORT",
            ],
            "1,0,EAST",
        ),
        (
            [
                "PLACE 4,4,SOUTH",
                "MOVE",
                "REPORT",
            ],
            "4,3,SOUTH",
        ),
        (
            [
                "PLACE 4,4,WEST",
                "MOVE",
                "REPORT",
            ],
            "3,4,WEST",
        ),
    ],
    ids=[
        "Move NORTH",
        "Move EAST",
        "Move SOUTH",
        "Move WEST",
    ],
)
def test_move_command(
    command_list: list[str],
    expected_report: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test the move command correctly moves the robot.

    Places the robot in the SOUTH WEST corner and tries to move NORTH, then
    places again and tries to move EAST.
    Places the robot in the NORTH EAST corner and tries to move SOUTH, then
    places again and tries to move WEST.

    Verifies requirements #5, #11 in the README
    """
    expected_report_msg = f"Robot position is {expected_report}"
    with patch_input(command_list):
        main()
        assert expected_report_msg in caplog.messages


@pytest.mark.parametrize(
    ("command_list", "expected_report"),
    [
        (
            [
                "PLACE 0,0,NORTH",
                "LEFT",
                "LEFT",
                "LEFT",
                "LEFT",
                "LEFT",
                "REPORT",
            ],
            "0,0,WEST",
        ),
        (
            [
                "PLACE 0,0,NORTH",
                "RIGHT",
                "RIGHT",
                "RIGHT",
                "RIGHT",
                "RIGHT",
                "REPORT",
            ],
            "0,0,EAST",
        ),
    ],
    ids=[
        "Left Turns",
        "Right Turns",
    ],
)
def test_left_right_commands(
    command_list: list[str],
    expected_report: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test the left and right commands change the direction of the robot.

    Verifies requirement #12 in the README
    """
    expected_report_msg = f"Robot position is {expected_report}"
    with patch_input(command_list):
        main()
        assert expected_report_msg in caplog.messages


@pytest.mark.parametrize(
    ("command_list", "expected_report"),
    [
        (
            [
                "PLACE 0,0,NORTH",
                "MOVE",
                "REPORT",
            ],
            "0,1,NORTH",
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

    Verifies requirement #13 in the README.

    Uses test cases found in the briefing document.
    """
    expected_report_msg = f"Robot position is {expected_report}"
    with patch_input(command_list):
        main()
        assert expected_report_msg in caplog.messages


def test_help_command(caplog: pytest.LogCaptureFixture) -> None:
    """Test the help command output is correct."""
    expected_msg = """
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
    with patch_input(["HELP"]):
        main()
        assert expected_msg in caplog.messages


def test_invalid_commands(caplog: pytest.LogCaptureFixture) -> None:
    """Test invalid commands are ignored."""
    expected_report_msgs = [
        "Placed the robot at 0,0,NORTH",
        "Invalid command format",
        "Unknown command: 0,0,NORTH",
        "Unknown command: PUT",
        "Invalid PLACE arguments given",
        "Unknown command: GO",
        "Invalid command format",
        "Invalid command format",
    ]
    with patch_input(
        [
            "PLACE 0,0,NORTH",
            "PLACE 0, 0, NORTH",
            "0,0,NORTH PLACE",
            "PUT -1,0,NORTH",
            "PLACE NORTH,0,1",
            "GO FORWARD",
            "MOVE THE ROBOT FORWARD",
            "",
        ]
    ):
        main()
        assert is_msg_sequence_in_logs(caplog.messages, expected_report_msgs)


def test_imperfect_commands(caplog: pytest.LogCaptureFixture) -> None:
    """Test imperfect commands are still accepted.

    The command is accepted regardless of capitalisation.

    Supplying an argument after a command that does not expect an argument
    results in the command still being accepted, but the argument is ignored.
    """
    expected_report_msgs = [
        "Placed the robot at 0,0,NORTH",
        "Placed the robot at 0,0,NORTH",
        "Moving North...",
        "Turning to face EAST",
        "Turning to face NORTH",
        "Robot position is 0,1,NORTH",
    ]
    with patch_input(
        [
            "PLACE 0,0,NORTH",
            "pLaCe 0,0,north",
            "MOVE FORWARD",
            "RIGHT 90deg",
            "LEFT TURN",
            "REPORT POSITION",
        ]
    ):
        main()
        assert is_msg_sequence_in_logs(caplog.messages, expected_report_msgs)
