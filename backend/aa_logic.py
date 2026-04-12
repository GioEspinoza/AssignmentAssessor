from datetime import datetime
import math


def add_task(completed, course, task, difficulty, used_hours, to_use_hours,date_completed=None, due_date=None):
    
    value = {
        "course":course,
        "task":task,
        "difficulty":difficulty,
        "completed":completed
    }
    if completed:
        value["date_completed"] = date_completed
        value["hours"] = used_hours
    else:
        value["due_date"] = due_date
        value["hours"] = to_use_hours
        
        
        
    return value

def urgent_sort(tasks): 
    incomp_tasks = [t for t in tasks if not t["completed"]]
    for t in incomp_tasks:
        t["priority"] = priority_calculation(t)

    # sort the incompleted tasks by priority level using priority formula, potentially account for due date later
    return sorted(incomp_tasks, key=lambda x: x["priority"], reverse=True)

def hours_per_day(hours, day):
    """Will return the recommended hours per day based off value = hours needed/days rem"""
    # if day is 0 set to 1
    if day <= 0:
        day = 1
    # the value value of the hours per day
    return round_down_to_two_decimals(hours / day)

def round_down_to_two_decimals(num):
    return math.floor(num * 100) / 100

def priority_calculation(task):
    """Will return the priority status of task based off difficulty*hours/days remaining"""

    # set due date to days left until task needs to be completed
    days_rem = days_left(task["due_date"])
    # if due date is 0 or overdue, priority should be very high
    if days_rem <= 0:
        days_rem = 1
    # return priority level based off formula (difficulty*hours)/ days left
    return (task["difficulty"] * task["hours"]) / days_rem

def is_not_empty(value):
    """check if value is empty"""
    return bool(value)

def is_in_range(value, low, high):
    """check object to see if in range"""
    try:
        num = int(value)
        return low <= num <= high
    except ValueError:
        return False

def valid_due_date(value):
    """check if date enterd is valid or not"""
    try:
        # must ensure both dates are the same object
        due = datetime.strptime(value, "%m-%d-%Y").date()
        today = datetime.today().date()
        return due >= today
    except ValueError:
        return False

def valid_comp_date(value):
    """check if date enterd is valid or not"""
    try:
        # must ensure both dates are the same object
        due = datetime.strptime(value, "%m-%d-%Y").date()
        today = datetime.today().date()
        return due <= today
    except ValueError:
        return False

def days_left(due_date):
    # using datetime to get todays date,
    today = datetime.today().date()
    # must convert due date to date value
    due = datetime.strptime(due_date, "%m-%d-%Y").date()
    # subtract both dates and only return the day value
    return (due - today).days

def is_diff(value):
    """check if difficulty entered is in range of difficulty"""
    return is_in_range(value, 1, 5)

def is_positive_int(value):
    """check if pos"""
    return value.isdigit() and int(value) > 0

def is_hours(value):
    """check if hours is pos"""
    return is_positive_int(value)

def check_incomp_tasks(tasks):
    """checks if there are any incompleted tasks"""
    return any(not task.get("completed", False) for task in tasks)