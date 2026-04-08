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
incomp_tasks = []

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
        ### main menu options ###
        ##addtask
        if choice == "1":
            choice_1(tasks)

        ## view all tasks
        elif choice == "2":
            view_all_tasks(tasks)
            menu_go_back()

        ## view urgent tasks, sorted by priority
        elif choice == "3":
            if incomp_tasks:
                print("\nUrgent Tasks\n")
                  # display most urgent tasks in detail, based off priority.
                for i, task in enumerate(urgent_sort(incomp_tasks), start=1):
                    print(
                    f"{i}. {task['course']} | {task['task']} |"
                    f"Difficulty: {task['difficulty']} | Due: {task['due_date']} |"
                    f"Hours: {task['hours']} | Priority:{task['priority']:.2f}"
                    )
                menu_go_back()
            
            else:
                print("No urgent tasks found.")
               
        ## study plan, sorted by priority, with hours per day recommendation based off days left until due date and hours needed
        elif choice == "4":
            if incomp_tasks:
                print("Study Plan")
                for i, task in enumerate(urgent_sort(incomp_tasks), start=1):
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
                menu_go_back()

            else:
                print("No incompleted tasks found.")
            
        ## mark task as completed, will show list of incompleted tasks, ask for user choice, confirm choice, and mark as completed if confirmed
        elif choice == "5":
                if not incomp_tasks:
                    print("No incomplete tasks to mark as completed.")
                    continue
                else:
                    mark_complete(urgent_sort(incomp_tasks))

        ## bye    
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


def user_choice_completed_task(counter):
    """Will check whether input is in range and valid, loop if not"""
    while True:
        choice = input("Enter the number of whichever task you completed: ")
        if choice.isdigit():
            choice = int(choice)

            if is_in_range(choice, 1, counter):
                return choice
        print("Not valid number! try again.")

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
            mark_complete(urgent_sort(tasks))
            break
        else:
            print("Not valid input, please try again!")

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
            choice_1(tasks)
            break
        else:
            print("Not valid input, please try again!")

def choice_1(tasks):
    #first prompt user for completion status
    is_comp = input("Is task already completed? [y/n]: ").lower().strip()
    #prompt for constant values
    constant_values = prompt_constant_values()
    course = constant_values["course"]
    task = constant_values["task"]
    difficulty = constant_values["difficulty"]
    completed = check_task_status(is_comp)

    if completed:
        comp_task = prompt_comp_task()
        date_completed = comp_task["date_completed"]
        used_hours = comp_task["hours"]
        due_date = None
        value = add_task(completed, course, task, difficulty, used_hours, None, date_completed, due_date)

    else:
        incomp_task = prompt_incomp_task()
        due_date = incomp_task["due_date"]
        to_use_hours = incomp_task["hours"]
        date_completed = None
        incomp_tasks.append(add_task(completed, course, task, difficulty, None, to_use_hours, None, due_date))
        value = add_task(completed, course, task, difficulty, None, to_use_hours, date_completed, due_date)
    print("\nOverview of task added:\n")
    print(value)
    rev_task(value, tasks)

def mark_complete(incomp_tasks):
    for i, task in enumerate(incomp_tasks, start=1):
        print(f"{i}. {task['course']} | {task['task']} | Due: {task['due_date']}")
    choice = user_choice_completed_task(len(incomp_tasks))
    print("Incompleted Tasks:\n")
    chosen = incomp_tasks[choice-1]
    print("\nOverview of choice:\n")
    print(
        f"{choice}. {chosen['course']} | {chosen['task']} | Due: {chosen['due_date']} "
    )
    rev_mark_comp(chosen, incomp_tasks)
        

def check_task_status(completion_prompt):
    """will check whether task is completed or not"""
    while True:
        if completion_prompt not in ["y", "n"]:
            print("Invalid input, please try again.")
            continue
        return completion_prompt == "y"

def end_aa(name):
    """exits program"""
    print(f"See ya {name}!")

def ask_until_valid(prompt, validator, error_msg):
    """simple prompt loop"""
    while True:
        value = input(prompt).strip()
        if validator(value):
            return value
        print(error_msg)

if __name__ == "__main__":
    main()
