from datetime import datetime, timedelta

import pytest

from backend import aa_logic


def formatted_date(days_from_today: int) -> str:
    return (datetime.today() + timedelta(days=days_from_today)).strftime("%m-%d-%Y")


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("1", True),
        ("5", True),
        ("0", False),
        ("6", False),
        ("abc", False),
    ],
)
def test_difficulty_range(value, expected):
    assert aa_logic.is_diff(value) is expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [("3.5", True), ("0", False), ("-1", False), ("", False), ("abc", False)],
)
def test_positive_hours(value, expected):
    assert bool(aa_logic.is_hours(value)) is expected


def test_date_validation():
    today = formatted_date(0)

    assert aa_logic.valid_due_date(today)
    assert aa_logic.valid_due_date(formatted_date(10))
    assert not aa_logic.valid_due_date(formatted_date(-1))
    assert aa_logic.valid_comp_date(today)
    assert aa_logic.valid_comp_date(formatted_date(-10))
    assert not aa_logic.valid_comp_date(formatted_date(1))
    assert not aa_logic.valid_due_date("not-a-date")


def test_return_task_builds_incomplete_assignment():
    task = aa_logic.return_task(
        False,
        "Algorithms",
        "Problem set",
        4,
        None,
        6.5,
        due_date="12-31-2099",
    )

    assert task == {
        "course": "Algorithms",
        "task": "Problem set",
        "difficulty": 4.0,
        "completed": False,
        "due_date": "12-31-2099",
        "hours": 6.5,
    }


def test_return_task_builds_completed_assignment():
    task = aa_logic.return_task(
        True,
        "Databases",
        "Schema project",
        3,
        4,
        None,
        date_completed="01-15-2026",
    )

    assert task["completed"] is True
    assert task["hours"] == 4.0
    assert task["date_completed"] == "01-15-2026"
    assert "due_date" not in task


def test_urgent_sort_excludes_completed_and_orders_priority():
    tasks = [
        {
            "course": "History",
            "task": "Essay",
            "completed": False,
            "difficulty": 2,
            "hours": 2,
            "due_date": formatted_date(4),
        },
        {
            "course": "Physics",
            "task": "Lab",
            "completed": False,
            "difficulty": 5,
            "hours": 8,
            "due_date": formatted_date(2),
        },
        {
            "course": "Art",
            "task": "Sketch",
            "completed": True,
            "difficulty": 1,
            "hours": 1,
            "date_completed": formatted_date(0),
        },
    ]

    result = aa_logic.urgent_sort(tasks)

    assert [task["course"] for task in result] == ["Physics", "History"]
    assert all(not task["completed"] for task in result)


def test_overdue_assignment_uses_one_day_for_priority():
    task = {
        "difficulty": 4,
        "hours": 3,
        "due_date": formatted_date(-3),
    }
    assert aa_logic.priority_calculation(task) == 12


def test_study_hours_round_down_and_handle_overdue():
    assert aa_logic.hours_per_day(10, 3) == 3.33
    assert aa_logic.hours_per_day(5, 0) == 5
    assert aa_logic.hours_per_day(5, -2) == 5


def test_alphabetical_tasks_is_case_insensitive():
    tasks = [{"course": "zoology"}, {"course": "Algorithms"}, {"course": "biology"}]

    assert [task["course"] for task in aa_logic.alphabetical_tasks(tasks)] == [
        "Algorithms",
        "biology",
        "zoology",
    ]
