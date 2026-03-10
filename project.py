import pyfiglet
proj_title = "Assignment Assesor"
ascii_aa = pyfiglet.figlet_format(proj_title) 
menu = ("""
1. Add task/completed task
2. View all tasks
3. View urgent tasks
4. Study plan
5. task completed
6. Close program
          """)
tasks = []
comp_tasks = []


def main():
    print(ascii_aa)
    print("Welcome to Assignment Assesor!!")
    while True:
        user = input("Input valid name:\n").strip()
        if check_name(user):
             break
    show_menu()
    while True:
        choice = input("Choice: ")
        if choice == "1":
             add_task()
        if choice == "2":
             view_all_tasks()
        if choice == "3":
             view_urgent()
        if choice == "4":
             study()
        if choice == "5":
             task_done()
        if choice == "6":
             end_aa(user)
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
        else:
            print(f"Hey {name}! Please select an option:")
            return True

def show_menu():
            print(menu)

def add_task():
    is_comp = check_task_status()
    comp_task = {}
    task = {}
    if is_comp():
        comp_task["course"] = input("Enter course name:\n")
        comp_task["task"] = input("Enter name of task:\n")
        comp_task["difficulty"] = input("Enter difficulty (1-5)\n").int()
        comp_task["due_date"] = input("Enter date completed (MM-DD-YYYY):\n")
        comp_task["hours"] = input("Enter hours taken:\n").int()
        comp_task["completed"] = True

    else:
        task["course"] = input("Enter course name: ")
        task["task"] = input("Enter name of task:\n")
        task["difficulty"] = input("Enter difficulty (1-5)\n").int()
        task["due_date"] = input("Enter due date (MM-DD-YYYY):\n")
        task["hours"] = input("Enter hours needed:\n").int()
        task["completed"] = False
        
    print("\nOverview of task added:\n")  

    if is_comp():
         print(comp_task)
         rev_task(comp_task)
    else:
         print(task)
         rev_task(task)
    
        
def view_all_tasks():
    ...

def view_urgent():
    ...

def study():
    ...

def task_done():
    ...

def end_aa(name):
     print(f"See ya {name}!")

def check_task_status():
     while True:
        check_task = input("Is task already completed? [y/n]: ").lower()
        if check_task != "y" or "n":
             print("Invalid input, please try again.")
             break
        return check_task == 'y'

def rev_task(task):
     review_task = input("\nIs this correct? [y/n]: ").lower()
     while True:
        if review_task == "y":
             tasks.append(task)
             print("Saved.")
             break
        elif review_task == "n":
             print("Restarting addition of task...\n")
             add_task()
        else:
             ("Not valid input, please try again!")
if __name__ == "__main__":
    main()