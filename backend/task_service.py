from datetime import date, datetime, timedelta

from backend import task_rules
from database import task_queries


def get_tasks(user_id):
    return task_queries.get_tasks(user_id)


def parse_task_date(date_value):
    if isinstance(date_value, datetime):
        return date_value.date()
    elif isinstance(date_value, date):
        return date_value

    for date_format in ("%Y-%m-%d", "%m-%d-%Y"):
        try:
            return datetime.strptime(
                str(date_value),
                date_format,
            ).date()
        except ValueError:
            continue

    return date.max


def get_due_state(due_date):
    days_remaining = (parse_task_date(due_date) - date.today()).days

    if days_remaining < 0:
        return "overdue"
    elif days_remaining <= 7:
        return "due_soon"
    else:
        return "upcoming"


def get_upcoming_tasks(user_id, limit=3):
    return select_upcoming_tasks(get_tasks(user_id), limit)


def select_upcoming_tasks(tasks, limit=3):
    upcoming_tasks = [
        task
        for task in tasks
        if not task_rules.is_completed(task)
        and task.get("due_date") is not None
    ]

    return sorted(
        upcoming_tasks,
        key=lambda task: parse_task_date(task["due_date"]),
    )[:limit]


def get_task_summary(tasks):
    return {
        "due_this_week": sum(
            1
            for task in tasks
            if task.get("due_date")
            and is_due_this_week(task["due_date"])
        ),
        "due_soon": sum(
            1
            for task in tasks
            if task.get("status") != "completed"
            and task.get("due_date")
            and get_due_state(task["due_date"]) == "due_soon"
        ),
        "estimated_workload": sum(
            task_rules.remaining_hours(task)
            for task in tasks
            if task.get("status") != "completed"
        ),
        "in_progress_tasks": sum(
            1
            for task in tasks
            if task.get("status") == "in_progress"
        ),
        "completed_tasks": sum(
            1
            for task in tasks
            if task.get("status") == "completed"
        ),
    }


def get_dashboard_summary(user_id):
    return get_task_summary(get_tasks(user_id))


def get_dashboard_data(user_id, upcoming_limit=3):
    tasks = get_tasks(user_id)
    return {
        "summary": get_task_summary(tasks),
        "upcoming_tasks": select_upcoming_tasks(
            tasks,
            upcoming_limit,
        ),
    }


def filter_tasks_by_status(tasks, status=None):
    if status is None:
        return tasks

    if not task_rules.is_valid_task_status(status):
        return tasks

    return [
        task
        for task in tasks
        if task.get("status") == status
    ]


def search_tasks(tasks, query):
    search_value = query.strip().casefold()
    if not search_value:
        return tasks

    return [
        task
        for task in tasks
        if search_value in task.get("task", "").casefold()
        or search_value in task.get("course", "").casefold()
    ]


def is_due_this_week(due_date):
    parsed_date = parse_task_date(due_date)
    if parsed_date == date.max:
        return False

    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week <= parsed_date <= end_of_week
