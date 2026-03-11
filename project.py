import pyfiglet
from datetime import datetime

proj_title = "Assignment Assessor"
ascii_aa = pyfiglet.figlet_format(proj_title)

menu = """
1. Add task
2. View all tasks
3. View urgent tasks
4. Study plan
5. Mark task as completed
6. Close program
"""
tasks = []

def main():
    print(ascii_aa)
    print("Welcome to Assignment Assessor!!")

    while True:
        user = input("Input valid name:\n").strip()
        if check_name(user):
            break

    while True:
        show_menu()
        choice = input("Choice: ").strip()
        if choice == "1":
            add_task()
        elif choice == "2":
            view_all_tasks()
        elif choice == "3":
            view_urgent()
        elif choice == "4":
            study()
        elif choice == "5":
            task_done()
        elif choice == "6":
            end_aa(user)
            break
        else:
            print("Not a valid input, please try again.")

def check_name(name):
    if not name:
        print("Not valid name! Please try again")
        return False
    if any(char.isdigit() for char in name):
        print("Not valid name! Please try again")
        return False
    if "  " in name:
        print("Not valid name! Please try again")
        return False

    print(f"Hey {name}! Please select an option:")
    return True

def show_menu():
    print(menu)

def add_task():
    is_comp = check_task_status()
    value = {}

    value["course"] = ask_until_valid(
        "Enter course name:\n", is_not_empty, "Course name cannot be empty."
    )
    value["task"] = ask_until_valid(
        "Enter name of task:\n", is_not_empty, "Task name cannot be empty."
    )
    value["difficulty"] = int(
        ask_until_valid(
            "Enter difficulty (1-5):\n",
            is_diff,
            "Difficulty must be an integer between 1 and 5.",
        )
    )

    if is_comp:
        value["date_completed"] = ask_until_valid(
            "Enter date completed (MM-DD-YYYY):\n",
            valid_date,
            "Date must be in the format MM-DD-YYYY.",
        )
        value["hours"] = int(
            ask_until_valid(
                "Enter hours used:\n",
                is_hours,
                "Hours used must be a positive integer.",
            )
        )
        value["completed"] = True
    else:
        value["due_date"] = ask_until_valid(
            "Enter due date (MM-DD-YYYY):\n",
            valid_date,
            "Date must be in the format MM-DD-YYYY.",
        )
        value["hours"] = int(
            ask_until_valid(
                "Enter hours needed:\n",
                is_hours,
                "Hours needed must be a positive integer.",
            )
        )
        value["completed"] = False

    print("\nOverview of task added:\n")
    print(value)
    rev_task(value)

def view_all_tasks():
    if not tasks:
        print("No tasks to display.")
        return
    for i, task in enumerate(tasks, start=1):
        print(i, task)

def view_urgent():
    incomp = [task for task in tasks if not task["completed"]]
    if not incomp:
        print("No urgent tasks found.")
        return
    
    sorted_tasks = sorted(incomp,keys=priority_calculation,reverse=True)

    print("\nUrgent Tasks\n")
    for i, task in enumerate(sorted_tasks, start=1):
        priority = priority_calculation(task)
        print(
            f"{i}. {task["course"]} | {task["task"]} |"
            f"Difficulty: {task["difficulty"]} | Due: {task["due_date"]} |"
            f"Hours: {task["hours"]} | Priority:{priority:.2f}"
            )

def priority_calculation(task):
    days_rem = days_left(task["due_date"])
    if days_rem <= 0:
        days_rem = 1
    return ((task["difficulty"]*task["hours"])/days_rem)

def days_left(due_date):
    today = datetime.today().date()
    due = datetime.strptime(due_date, "%m-%d-%Y").date()
    return(due-today).days

def study():
    pass

def task_done():
    pass

def end_aa(name):
    print(f"See ya {name}!")

def check_task_status():
    while True:
        check_task = input("Is task already completed? [y/n]: ").lower().strip()
        if check_task not in ["y", "n"]:
            print("Invalid input, please try again.")
            continue
        return check_task == "y"

def rev_task(task):
    while True:
        review_task = input("\nIs this correct? [y/n]: ").lower().strip()
        if review_task == "y":
            tasks.append(task)
            print("Saved.")
            break
        elif review_task == "n":
            print("Restarting addition of task...\n")
            add_task()
            break
        else:
            print("Not valid input, please try again!")

def ask_until_valid(prompt, validator, error_msg):
    while True:
        value = input(prompt).strip()
        if validator(value):
            return value
        print(error_msg)

def is_not_empty(value):
    return bool(value)

def is_in_range(value, low, high):
    if not value.isdigit():
        return False
    num = int(value)
    return low <= num <= high


def valid_date(value):
    try:
        datetime.strptime(value, "%m-%d-%Y")
        return True
    except ValueError:
        return False

def is_diff(value):
    return is_in_range(value, 1, 5)

def is_positive_int(value):
    return value.isdigit() and int(value) > 0

def is_hours(value):
    return is_positive_int(value)

if __name__ == "__main__":
    main()