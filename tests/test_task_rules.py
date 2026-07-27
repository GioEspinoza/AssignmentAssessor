from datetime import datetime, timedelta

import pytest

from backend import task_rules, validation


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
    assert validation.is_diff(value) is expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [("3.5", True), ("0", False), ("-1", False), ("", False), ("abc", False)],
)
def test_positive_hours(value, expected):
    assert bool(validation.is_hours(value)) is expected


def test_date_validation():
    today = formatted_date(0)

    assert validation.valid_due_date(today)
    assert validation.valid_due_date(formatted_date(10))
    assert not validation.valid_due_date(formatted_date(-1))
    assert validation.valid_comp_date(today)
    assert validation.valid_comp_date(formatted_date(-10))
    assert not validation.valid_comp_date(formatted_date(1))
    assert not validation.valid_due_date("not-a-date")


def test_return_task_builds_not_started_assignment():
    task = task_rules.return_task(
        "not_started",
        "Algorithms",
        "Problem set",
        4,
        6.5,
        due_date="12-31-2099",
    )

    assert task == {
        "course": "Algorithms",
        "task": "Problem set",
        "difficulty": 4.0,
        "status": "not_started",
        "estimated_hours": 6.5,
        "hours_used": None,
        "due_date": "12-31-2099",
        "date_completed": None,
    }


def test_return_task_builds_completed_assignment():
    task = task_rules.return_task(
        "completed",
        "Databases",
        "Schema project",
        3,
        None,
        4,
        date_completed="01-15-2026",
    )

    assert task["status"] == "completed"
    assert task["hours_used"] == 4.0
    assert task["date_completed"] == "01-15-2026"
    assert task["due_date"] is None


def test_return_task_builds_in_progress_assignment():
    task = task_rules.return_task(
        "in_progress",
        "Databases",
        "Schema project",
        3,
        8,
        2.5,
        due_date="12-31-2099",
    )

    assert task["status"] == "in_progress"
    assert task["estimated_hours"] == 8.0
    assert task["hours_used"] == 2.5
    assert task_rules.remaining_hours(task) == 5.5


def test_return_task_rejects_invalid_status():
    with pytest.raises(ValueError, match="Invalid task status"):
        task_rules.return_task(
            "pending",
            "Databases",
            "Schema project",
            3,
        )


def test_urgent_sort_excludes_completed_and_orders_priority():
    tasks = [
        {
            "course": "History",
            "task": "Essay",
            "status": "not_started",
            "difficulty": 2,
            "estimated_hours": 2,
            "due_date": formatted_date(4),
        },
        {
            "course": "Physics",
            "task": "Lab",
            "status": "in_progress",
            "difficulty": 5,
            "estimated_hours": 8,
            "due_date": formatted_date(2),
        },
        {
            "course": "Art",
            "task": "Sketch",
            "status": "completed",
            "difficulty": 1,
            "hours_used": 1,
            "date_completed": formatted_date(0),
        },
    ]

    result = task_rules.urgent_sort(tasks)

    assert [task["course"] for task in result] == ["Physics", "History"]
    assert all(task["status"] != "completed" for task in result)


def test_overdue_assignment_uses_one_day_for_priority():
    task = {
        "difficulty": 4,
        "estimated_hours": 3,
        "due_date": formatted_date(-3),
    }
    assert task_rules.priority_calculation(task) == 12


def test_study_hours_round_down_and_handle_overdue():
    assert task_rules.hours_per_day(10, 3) == 3.33
    assert task_rules.hours_per_day(5, 0) == 5
    assert task_rules.hours_per_day(5, -2) == 5


def test_alphabetical_tasks_is_case_insensitive():
    tasks = [{"course": "zoology"}, {"course": "Algorithms"}, {"course": "biology"}]

    assert [task["course"] for task in task_rules.alphabetical_tasks(tasks)] == [
        "Algorithms",
        "biology",
        "zoology",
    ]
