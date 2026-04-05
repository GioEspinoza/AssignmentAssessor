from datetime import datetime
import math




def add_task(tasks, completed, course, task, difficulty, date_completed=None, due_date=None,used_hours=None, to_use_hours=None):
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

# function that will return list of incompleted urgent tasks
def urgent_sort(tasks):
    sorted_tasks = []
    for task in tasks:
        if not task["completed"]:
            sorted_tasks.append(task)
    for task in sorted_tasks:
        task["priority"] = priority_calculation(task)
    # sort the incompleted tasks by priority level using priority formula, potentially account for due date later
    sorted_tasks = sorted(sorted_tasks, key=lambda x: x["priority"], reverse=True)
    return sorted_tasks

def priority_calculation(task):
    """Will return the priority status of task based off difficulty*hours/days remaining"""

    # set due date to days left until task needs to be completed
    days_rem = days_left(task["due_date"])
    # if due date is 0 or overdue, priority should be very high
    if days_rem <= 0:
        days_rem = 1
    # return priority level based off formula (difficulty*hours)/ days left
    return (task["difficulty"] * task["hours"]) / days_rem


# assign a variable with the amount of days left until due date
def days_left(due_date):
    # using datetime to get todays date,
    today = datetime.today().date()
    # must convert due date to date value
    due = datetime.strptime(due_date, "%m-%d-%Y").date()
    # subtract both dates and only return the day value
    return (due - today).days


def study(tasks):
    # filter out for only incomplete task
    # we only want incompleted tasks to study for.
    incomp = [task for task in tasks if not task["completed"]]
    if not incomp:
        print("No urgent tasks found.")
        return
    # calculate for priority in each task
    for task in incomp:
        task["priority"] = priority_calculation(task)
    # sort list by most urgent
    sorted_tasks = sorted(incomp, key=priority_calculation, reverse=True)

    print("Study Plan")

    # display organized list
    for i, task in enumerate(sorted_tasks, start=1):
        days_rem = days_left(task["due_date"])
        hours_day = hours_per_day(task["hours"], days_rem)
        if days_rem > 0:
            print(
                f"{i}. {task['course']} | {task['task']} |"
                f"Difficulty: {task['difficulty']} | Days Left: {days_rem} |"
                f"Hours suggested per day: {hours_day} | "
            )
        else:
            print(
                f"{i}. {task['course']} | {task['task']} |"
                f"Difficulty: {task['difficulty']} | Days left: OVERDUE|"
            )


def hours_per_day(hours, day):
    """Will return the recommended hours per day based off value = hours needed/days rem"""
    # if day is 0 set to 1
    if day <= 0:
        day = 1
    # the value value of the hours per day
    return round_down_to_two_decimals(hours / day)


# function that simplifes the rounding process
def round_down_to_two_decimals(num):
    return math.floor(num * 100) / 100


def task_done(tasks):
    # seperating tasks by completion status, if all are completed loop back
    incomp = [task for task in tasks if not task["completed"]]
    if not incomp:
        print("No incomplete tasks found.")
        return
    # organize task into numbered
    for i, task in enumerate(incomp, start=1):
        print(f"{i}. {task['course']} | {task['task']} | Due: {task['due_date']}")
    # get and validate user choice
    choice = user_choice_completed_task(len(incomp))
    index = choice - 1
    chosen = incomp[index]

    # confirm user choice before saving
    print("\nOverview of choice:\n")
    print(
        f"{choice}. {chosen['course']} | {chosen['task']} | Due: {chosen['due_date']} "
    )
    rev_mark_comp(chosen, tasks)


def rev_mark_comp(task, tasks):
    """will confirm user choice in task to be marked for completion"""
    while True:
        review_task = input("\nIs this correct? [y/n]: ").lower().strip()
        if review_task == "y":
            task["completed"] = True
            # strftime formats date objects as strings.
            task["date_completed"] = datetime.today().strftime("%m-%d-%Y")
            print(f"Marked as compelted")
            break
        elif review_task == "n":
            print("Restarting choice of task...\n")
            task_done(tasks)
            break
        else:
            print("Not valid input, please try again!")


def user_choice_completed_task(counter):
    """Will check whether input is in range and valid, loop if not"""
    while True:
        choice = input("Enter the number of whichever task you completed: ")
        if choice.isdigit():
            choice = int(choice)

            if is_in_range(choice, 1, counter):
                return choice
        print("Not valid number! try again.")


def end_aa(name):
    """exits program"""
    print(f"See ya {name}!")


def check_task_status(completion_prompt):
    """will check whether task is completed or not"""
    while True:
        if completion_prompt not in ["y", "n"]:
            print("Invalid input, please try again.")
            continue
        return completion_prompt == "y"


def rev_task(task, tasks):
    """will check if users input for whether task is completed is valid"""
    while True:
        review_task = input("\nIs this correct? [y/n]: ").lower().strip()
        if review_task == "y":
            tasks.append(task)
            print("Saved.")
            break
        elif review_task == "n":
            print("Restarting addition of task...\n")
            add_task(tasks)
            break
        else:
            print("Not valid input, please try again!")


def ask_until_valid(prompt, validator, error_msg):
    """simple prompt loop"""
    while True:
        value = input(prompt).strip()
        if validator(value):
            return value
        print(error_msg)


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


def is_diff(value):
    """check if difficulty entered is in range of difficulty"""
    return is_in_range(value, 1, 5)


def is_positive_int(value):
    """check if pos"""
    return value.isdigit() and int(value) > 0


def is_hours(value):
    """check if hours is pos"""
    return is_positive_int(value)
