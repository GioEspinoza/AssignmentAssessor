import pyfiglet
from aa_logic import *

# save title in ascii format
proj_title = "Assignment Assessor"
ascii_aa = pyfiglet.figlet_format(proj_title)

# save menu for easy reprints
menu = """
1. Add task
2. View all tasks
3. View urgent tasks
4. Study plan
5. Mark task as completed
6. Close program
"""

# empty list to hold tasks
tasks = []


# Print and welcome to program, check for user name, and menu loop
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
            #first prompt user for completion status
            is_comp = input("Is task already completed? [y/n]: ").lower().strip()
            #prompt for constant values
            constant_values = prompt_constant_values()
            course, task, difficulty = constant_values["course"],constant_values["task"],constant_values["difficulty"]
            completed = check_task_status(is_comp)

            if completed:
                comp_task = prompt_comp_task()
                date_completed = comp_task["date_completed"]
                hours = comp_task["hours"]
                due_date = None
                value = add_task(tasks, completed, course, task, difficulty,hours, date_completed, due_date)

            else:
                incomp_task = prompt_incomp_task()
                due_date = incomp_task["due_date"]
                hours =  incomp_task["hours"]
                date_completed = None
                value = add_task(tasks, completed, course, task, difficulty, hours, due_date, date_completed)
            

            print("\nOverview of task added:\n")
            print(value)
            rev_task(value, tasks)

            menu_go_back()

        elif choice == "2":
            view_all_tasks(tasks)
            menu_go_back()

        elif choice == "3":
            if not urgent_sort(tasks):
                print("No urgent/incompleted tasks found.")
                continue
            else:
                print("\nUrgent Tasks\n")
                  # display most urgent tasks in detail, based off priority.
                for i, task in enumerate(urgent_sort(tasks), start=1):
                    print(
                    f"{i}. {task['course']} | {task['task']} |"
                    f"Difficulty: {task['difficulty']} | Due: {task['due_date']} |"
                    f"Hours: {task['hours']} | Priority:{task['priority']:.2f}"
                    )
            menu_go_back()
                
        elif choice == "4":
            study(tasks)
            menu_go_back()
        elif choice == "5":
            task_done(tasks)
            menu_go_back()
        elif choice == "6":
            end_aa(user)
            break
        else:
            print("Not a valid input, please try again.")


# function to show menu
def show_menu():
    print(menu)

def prompt_constant_values():
    constant_values = {}
    constant_values["course"] = ask_until_valid(
        "Enter course name:\n", is_not_empty, "Course name cannot be empty."
    )
    constant_values["task"] = ask_until_valid(
        "Enter name of task:\n", is_not_empty, "Task name cannot be empty."
    )
    constant_values["difficulty"] = int(
        ask_until_valid(
            "Enter difficulty (1-5):\n",
            is_diff,
            "Difficulty must be an integer between 1 and 5.",
        )
    )

    return constant_values

def prompt_incomp_task():
    incomp_values = {}

    incomp_values["due_date"] = ask_until_valid(
            "Enter due date (MM-DD-YYYY):\n",
            valid_due_date,
            "Invalid Date/Date Format",
        )
    incomp_values["hours"] = int(
            ask_until_valid(
                "Enter hours needed:\n",
                is_hours,
                "Invalid input",
            )
        )
    return incomp_values

def prompt_comp_task():
    comp_values = {}

    comp_values["date_completed"] = ask_until_valid(
            "Enter date completed (MM-DD-YYYY):\n",
            valid_comp_date,
            "Invalid Date/Date Format",
        )
    comp_values["hours"] = int(
            ask_until_valid(
                "Enter hours used:\n",
                is_hours,
                "Invalid input",
            )
        )
    return comp_values

# simply show all task, loop back to menu if no task available
def view_all_tasks(tasks):
    if not tasks:
        print("No tasks to display.")
        return
    print("List of tasks:\n")
    for i, task in enumerate(tasks, start=1):
        print(i, task)

# ensuring name is not empty, no numbers, and no double spaces. Looping if name isnt valid, welcoming if it is valid.
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

def menu_go_back():
    while True:
        user_input = input("\nType menu to go back to menu: ")
        if user_input.lower() == "menu":
            break

if __name__ == "__main__":
    main()
