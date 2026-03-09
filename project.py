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
        name = input("Input valid name:\n")
        if name == "":
            print("Not valid name!")
            continue
        if any(char.isdigit() for char in name):
            print("Not valid name!")
        else:
            break
    
    while True:
        print(menu)
        choice = input("Choice: ")
        
        if choice == "6":
            break


def function_1():
    ...


def function_2():
    ...


def function_n():
    ...


if __name__ == "__main__":
    main()
