import math

from backend.validation import days_left


TASK_STATUSES = (
    "not_started",
    "in_progress",
    "completed",
)


def is_valid_task_status(status):
    return status in TASK_STATUSES


def is_completed(task):
    return task.get("status") == "completed"


def return_task(
    status,
    course,
    task,
    difficulty,
    estimated_hours=None,
    hours_used=None,
    date_completed=None,
    due_date=None,
):
    if not is_valid_task_status(status):
        raise ValueError("Invalid task status.")

    return {
        "course": course,
        "task": task,
        "difficulty": float(difficulty),
        "status": status,
        "estimated_hours": (
            float(estimated_hours)
            if estimated_hours is not None
            else None
        ),
        "hours_used": (
            float(hours_used)
            if hours_used is not None
            else None
        ),
        "date_completed": date_completed,
        "due_date": due_date,
    }


def urgent_sort(tasks):
    incomplete_tasks = [
        task for task in tasks
        if not is_completed(task)
    ]

    for task in incomplete_tasks:
        task["priority"] = priority_calculation(task)

    return sorted(
        incomplete_tasks,
        key=lambda task: task["priority"],
        reverse=True,
    )


def hours_per_day(hours, day):
    if day <= 0:
        day = 1
    return round_down_to_two_decimals(hours / day)


def round_down_to_two_decimals(num):
    return math.floor(num * 100) / 100


def priority_calculation(task):
    days_remaining = days_left(task["due_date"])
    if days_remaining <= 0:
        days_remaining = 1

    return (
        float(task["difficulty"])
        * remaining_hours(task)
    ) / days_remaining


def remaining_hours(task):
    estimated_hours = float(task.get("estimated_hours") or 0)
    hours_used = float(task.get("hours_used") or 0)
    return max(estimated_hours - hours_used, 0)


def check_incomp_tasks(tasks):
    return any(not is_completed(task) for task in tasks)


def alphabetical_tasks(tasks):
    return sorted(
        tasks,
        key=lambda task: task["course"].lower(),
    )
