import pyfiglet
proj_title = "Assignment Assesor"
ascii_aa = pyfiglet.figlet_format(proj_title) 
menu = ("""
1. Add task
2. View all tasks
3. View urgent tasks
4. Study plan
5. task completed
6. Close program
          """)



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
        if choice == "6":
            print(f"See ya {user}!")
            break

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



def function_n():
    ...


if __name__ == "__main__":
    main()
