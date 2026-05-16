#import sys
#from pathlib import Path
from datetime import date

from backend import storage, auth, aa_logic
import customtkinter as ctk

user_data = storage.load_user_prof()
tasks = storage.load_data()

aa_app = ctk.CTk()

#set title and window size
aa_app.title('Assignment Assessor')
aa_app.geometry('800x600')

#set title text
aa_title = ctk.CTkLabel(
    aa_app, 
    pady=25,
    text='Assignment Assessor',
    font=('Terminal',50),
    fg_color='grey',
    corner_radius=10
)

#encapsulate login screen
def login_screen():
    #instantiate welcoming substitute
    aa_subtitle = ctk.CTkLabel(aa_app)

    #instatiante authentication frame
    authentication_frame = ctk.CTkFrame(
        aa_app, 
        width=400, 
        height=300,
        corner_radius=15
    )

    #instantiate and configure username and password text boxes
    password_entry = ctk.CTkEntry(
        authentication_frame
    )
    password_entry.configure(
            placeholder_text="Password",
            placeholder_text_color='white',
            font=('Terminal', 15),
            show="*"
        )

    username_entry = ctk.CTkEntry(
        authentication_frame
    )
    username_entry.configure(
        placeholder_text='Username',
        placeholder_text_color='white',
        font=('Terminal', 15)
    )

    #instantiate label for invalid password/usernames
    invalid_label = ctk.CTkLabel(
            authentication_frame,
            font=('Terminal', 15),
            bg_color='transparent',
            text_color='red',
            text=''        
        )

    #instantiate buttons for register and log in
    log_in_button = ctk.CTkButton(
        authentication_frame,
        corner_radius=10,
        text='Log in',
        font=("Terminal", 25),
        command = lambda: log_in(
            password_entry.get(),
            invalid_label,
            authentication_frame,
            aa_subtitle
        )
    )

    register_button = ctk.CTkButton(
        authentication_frame,
        corner_radius=20,
        text= 'Register',
        font=("Terminal", 25),
        command= lambda: new_user(
            username_entry.get(),
            password_entry.get(),
            invalid_label,
            authentication_frame,
            aa_subtitle
        )
        )

    #if user data is none, set up registration page
    if user_data is None:
        aa_subtitle.configure(
            text='Welcome new User! Please register',
            font=('Terminal',25))
        aa_subtitle.pack(pady=10)

        username_entry.pack(
            pady=20
        )
        password_entry.pack(
            pady=10    
        )
        register_button.pack(
            pady=30
        )

    #if user has data, set up log in page
    else:
        aa_subtitle.configure(
            text=f"Welcome {user_data.get('username')}, Please log in",
            font=('Terminal',25)
        )
        aa_subtitle.pack(pady=10)

        password_entry.pack(
            pady=70
        )

        log_in_button.pack(
            pady=20
        )
    authentication_frame.pack(pady=20, expand=True)
    authentication_frame.pack_propagate(False)
    
#function that will register new user
def new_user(username_entry, password_entry, invalid_label, authentication_frame, aa_subtitle):
    global user_data
    #check if user and password are valid
    valid, message = auth.check_new_name(username_entry)
    passvalid, passmessage = auth.check_new_pass(password_entry)
    
    if not valid:
        #if not refresh label for invalid inputs
        invalid_label.configure(
            text=message
        )
        invalid_label.pack(
            pady=10
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return
    
    if not passvalid:
        #if not refresh label for invalid inputs
        invalid_label.configure(
            text=passmessage
        )
        invalid_label.pack(
            pady=10
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return
        
    storage.save_user_prof(
            username_entry,
            auth.hash_password(password_entry)
            )
    
    user_data = storage.load_user_prof()

    authentication_frame.destroy()
    aa_title.pack_forget()
    aa_subtitle.pack_forget()
    menu_screen()
                
#function that will authenticate old user
def log_in(password_entry, invalid_label, authentication_frame, aa_subtitle):
    #load in saved password
    if not auth.check_hpassword(user_data.get('hpassword'), password_entry):
        #if not refresh label for invalid inputs
        invalid_label.configure(
            text="Incorrect password"
         )
        invalid_label.pack(
            pady=10
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return
    
    authentication_frame.destroy()
    aa_title.configure(
        font=("Terminal", 40),
        pady=5
    )
    aa_subtitle.pack_forget()
    menu_screen()

#will show menu after authencation
def menu_screen():
    #instantiate menu frame
    menu_frame = ctk.CTkFrame(
        aa_app,
        bg_color='transparent',
        corner_radius=10
    )

    #instantiate exit button
    quit_button = ctk.CTkButton(
        aa_app,
        font=('Terminal', 20),
        text="Exit",
        command=lambda:back_to_login(menu_frame, quit_button)
        )

    #instantiate menu buttons
    add_task_button = ctk.CTkButton(
        menu_frame,
        font=('Terminal', 20),
        text="Add Task",
        command= lambda: add_task_gui(menu_frame, quit_button)
    )

    view_task_button = ctk.CTkButton(
        menu_frame,
        font=('Terminal', 20),
        text="View Task(s)",
        command= lambda: view_tasks_gui(menu_frame, quit_button, tasks)
        )
    
    view_urgent_button = ctk.CTkButton(
        menu_frame,
        font=('Terminal', 20),
        text="View Urgent(s)",
        command= lambda: view_urgents_gui(menu_frame, quit_button)
        )
    
    study_button = ctk.CTkButton(
        menu_frame,
        font=('Terminal', 20),
        text="Study Plan",
        command= lambda: study_plan_gui(menu_frame, quit_button)
        )
    
    completed_button = ctk.CTkButton(
        menu_frame,
        font=('Terminal', 20),
        text="Mark as Complete",
        command= lambda: mark_completed_gui(menu_frame, quit_button)
        )

    #pack frame
    menu_frame.pack(
        pady=20,
        padx=250,
        fill ='both', 
        expand = 1
    )

    #pack buttons
    add_task_button.pack(
        pady=25
    )
    view_task_button.pack(
        pady=25
    )
    view_urgent_button.pack(
        pady=25
    )
    study_button.pack(
        pady=25
    )
    completed_button.pack(
        pady=25
    )

    #pack exit button
    quit_button.pack(
        pady=10
    )

#add task function
def add_task_gui(frame, button_or_label):
    #make window bigger
    aa_app.geometry('900x800')

    #instantiate label for invalid password/usernames
    invalid_label = ctk.CTkLabel(
            aa_app,
            font=('Terminal', 25),
            bg_color='transparent',
            text_color='red',
            text=''        
        )
   
    #instatiate frame for add task inputs
    add_task_frame = ctk.CTkFrame(
        aa_app,
        bg_color='transparent',
        corner_radius=10
    )

    #instantiate and configure course text box
    course_entry = ctk.CTkEntry(
        add_task_frame,
        placeholder_text="Course Name",
        placeholder_text_color='white',
        font=('Terminal', 15)
    )

    task_entry = ctk.CTkEntry(
        add_task_frame,
        placeholder_text='Task Name',
        placeholder_text_color='white',
        font=('Terminal', 15)
    )

    #instantiate compelted check box
    completed_box = ctk.CTkCheckBox(
        add_task_frame,
        text="Is task completed?",
        checkmark_color='green',
        fg_color='white',
        hover_color="white"
    )

    #instatiate difficulty label and scale
    difficulty_label = ctk.CTkLabel(
        add_task_frame,
        text="On a scale of 1-5, how difficult?",
        font=("Terminal", 15)
    )
    difficulty_scale = ctk.CTkSlider(
        add_task_frame,
        corner_radius=10,
        fg_color='green',
        button_color='white',
        button_hover_color='white',
        button_corner_radius=10,
        border_color='transparent',
        number_of_steps=4,
        from_=1,
        to=5,
        progress_color='red',
    )

    #instantiate hours label and entry point
    hours_label = ctk.CTkLabel(
        add_task_frame,
        text="Input hours needed/used:",
        font=("Terminal", 15)
    )
    hours_entry = ctk.CTkEntry(
        add_task_frame,
        placeholder_text='Hours',
        placeholder_text_color='white',
        font=('Terminal', 15)
    )

    #instatiate data label and entry point
    date_label = ctk.CTkLabel(
        add_task_frame,
        text="Input date due/completed:",
        font=("Terminal", 15)
    )
    date_entry = ctk.CTkEntry(
        add_task_frame,
        placeholder_text='Date',
        placeholder_text_color='white',
        font=('Terminal', 15)
    )
    
    #instantiate submit button
    submit_button = ctk.CTkButton(
        add_task_frame,
        text='Submit Task',
        font=('Terminal', 20),
        command= lambda: submit_task_handle(
            bool(completed_box.get()),
            course_entry.get().strip(),
            task_entry.get().strip(),
            int(difficulty_scale.get()),            
            hours_entry.get(),
            date_entry.get(),
            invalid_label,
            add_task_frame,
            inner_quit_button
        )
    )
    #quit button back to menu
    inner_quit_button = ctk.CTkButton(
        add_task_frame,
        text="Cancel",
        font=('Terminal', 15),
        command= lambda: back_to_menu(add_task_frame, inner_quit_button)
    )

    #unshow menu frame  if coming from menu and then show task frame
    frame.destroy()
    add_task_frame.pack(
        pady=100,
        padx=200,
        fill ='both', 
        expand = 1
    )
    
    #show task frame inputs
    course_entry.pack(
        pady=20
    )
    task_entry.pack(
        pady=5
    )
    completed_box.pack(
        pady=5
    )
    difficulty_label.pack(
        pady=10
    )
    difficulty_scale.pack(
    )
    hours_label.pack(
        pady=10
    )
    hours_entry.pack()
    date_label.pack(
        pady=10
    )
    date_entry.pack()
    submit_button.pack(
        pady=5
    )

    #destroy outer quit button and show inner quit button
    button_or_label.destroy()
    inner_quit_button.pack(
        pady=10
    )
#submit task handle function
def submit_task_handle(is_comp, course, task, difficulty, hours, date, invalid_label, frame, quit_button):
    #check if task is completed or not
    if is_comp is False:
        #check if inputs for course and task are detected
        if check_not_empty_gui(course, task, hours) is False:
            invalid_label.configure(
                text="Empty inputs detected"
            )
            invalid_label.pack(
                pady=5
            )
            aa_app.after(2500, invalid_label.pack_forget)
            return
        
        #check for invalid hour input
        if aa_logic.is_hours(hours) is False:
            invalid_label.configure(
                text="Invalid hour input"
            )
            invalid_label.pack(
                pady=5
            )
            aa_app.after(2500, invalid_label.pack_forget)
            return

        #check for valid date format/input
        if aa_logic.valid_due_date(date) is False:
            invalid_label.configure(
                text="Invalid date input - (MM-DD-YYYY)"
            )
            invalid_label.pack(
                pady=5
            )
            aa_app.after(2500, invalid_label.pack_forget)
            return
        
        rev_task_gui(aa_logic.add_task(is_comp, course, task, difficulty, None, hours, None, date), frame, quit_button)
        return
    
    if check_not_empty_gui(course, task, hours) is False:
        invalid_label.configure(
            text="Empty inputs detected"
        )
        invalid_label.pack(
            pady=5
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return
    
    if aa_logic.is_hours(hours) is False:
        invalid_label.configure(
            text="Invalid hour input"
        )
        invalid_label.pack(
            pady=5
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return
    
    if aa_logic.valid_comp_date(date) is False:
        invalid_label.configure(
            text="Invalid date input - (MM-DD-YYYY)"
        )
        invalid_label.pack(
            pady=5
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return

    rev_task_gui(aa_logic.add_task(is_comp, course, task, difficulty, hours, None, date, None), frame, quit_button)
    return
#review task logic for gui
def rev_task_gui(task, frame, quit_button):
    #minimize window
    aa_app.geometry('800x600')
    #destroy previous frame to make space for frame to review task
    frame.destroy()
    quit_button.destroy()
    rev_task_frame = ctk.CTkFrame(
        aa_app,
        bg_color='transparent',
        corner_radius=10
    )
    
    #isntatiate label that will display task
    task_label= ctk.CTkLabel(
            rev_task_frame,
            font=('Terminal', 20),
        )
    
    #label that will show task saved if completed
    if task['completed'] is False:
        task_label.configure(
            text = f"Course Name: {task['course']}\n\nTask Name: {task['task']}\n\nCompletion Status: Not Completed\n\nLevel of Difficulty: {task['difficulty']}\n\nDue Date: {task['due_date']}"
        )
    else:
        task_label.configure(
                text = f"Course Name: {task['course']}\n\nTask Name: {task['task']}\n\nCompletion Status: Completed\n\nLevel of Difficulty: {task['difficulty']}\n\nDate Completed: {task['date_completed']}"
            )

    #construct frame for buttons
    yes_no_frame = ctk.CTkFrame(
        rev_task_frame,
        fg_color='transparent'
    )

    #construct yes/no buttons
    no_button = ctk.CTkButton(
        yes_no_frame,
        text='No',
        bg_color='transparent',
        fg_color='red',
        text_color='white',
        font=('Terminal', 15),
        corner_radius=10,
        hover_color='white',
        command= lambda: add_task_gui(rev_task_frame, task_recognized_label)
    )
    yes_button = ctk.CTkButton(
    yes_no_frame,
    text="Yes",
    bg_color='transparent',
    fg_color='green',
    font=('Terminal', 15),
    text_color='white',
    corner_radius=10,
    hover_color='white',
    command= lambda: submit_task(tasks, task, rev_task_frame, task_recognized_label)
    )
  
    #label to let user know the task was valid
    task_recognized_label = ctk.CTkLabel(
        aa_app,
        font=('Terminal', 20),
        text_color='green',
        text='Task valid! Please review'
    )
    
    #packing all elements
    task_recognized_label.pack(
        pady=5
    )
    rev_task_frame.pack(
        pady=25,
        padx=150,
        fill ='both', 
        expand = 1
    )
    task_label.pack(
        pady=50
    )

    yes_no_frame.pack(
        side="bottom",
        pady=20
    )
    yes_button.pack(
        side='left',
        padx=10
    )
    no_button.pack( 
        side='left',
        padx=10
    )
#logic for yes and no buttons
def submit_task(tasks, task, frame, button_or_label):
    tasks.append(task)
    storage.save_data(tasks)
    back_to_menu(frame, button_or_label)

#view task function
def view_tasks_gui(frame, button_or_label, tasks):
    aa_app.geometry('900x800')
    tasks = storage.load_data()

    frame.destroy()
    view_tasks_frame = ctk.CTkScrollableFrame(
        aa_app,
        bg_color='transparent',
        corner_radius=10
    )
    if tasks is False:
        sorted_tasks = aa_logic.alphabetical_tasks(tasks)
        for i, task in enumerate(sorted_tasks, start=1):
            task_label= ctk.CTkLabel(
                view_tasks_frame,
                font=('Terminal', 20),
            )
        
            if task['completed'] is False:
                task_label.configure(
                    text_color='red',
                    text = f"[{i}] - Course Name: {task['course']}\n\nTask Name: {task['task']}\n\nCompletion Status: Not Completed\n\nLevel of Difficulty: {task['difficulty']}\n\nDue Date: {task['due_date']}\n"
                )
            else:
                task_label.configure(
                    text_color='green',
                    text = f"[{i}] - Course Name: {task['course']}\n\nTask Name: {task['task']}\n\nCompletion Status: Completed\n\nLevel of Difficulty: {task['difficulty']}\n\nDate Completed: {task['date_completed']}\n"
                    )
            task_label.pack(
                pady=10
            )
    else:
        task_label=ctk.CTkLabel(
            view_tasks_frame,
            text="No tasks found!",
            font=("Terminal", 35, "bold")
        )
        task_label.pack(
            pady=200
        )

    inner_quit_button = ctk.CTkButton(
        aa_app,
        text="Cancel",
        font=('Terminal', 15),
        command= lambda: back_to_menu(view_tasks_frame, inner_quit_button)
    )
    
    view_tasks_frame.pack(
        pady=25,
        padx=150,
        fill ='both', 
        expand = 1
    )

    button_or_label.destroy()
    inner_quit_button.pack(
        pady=10
    )

#view urgents function
def view_urgents_gui(frame, button_or_label):
    aa_app.geometry('900x800')


    frame.destroy()
    view_urgents_frame = ctk.CTkScrollableFrame(
        aa_app,
        bg_color='transparent',
        corner_radius=10
    )
    if aa_logic.check_incomp_tasks(tasks):
        sorted_urgent_tasks = aa_logic.urgent_sort(tasks)
        for i, task in enumerate(sorted_urgent_tasks, start=1):
            task_label= ctk.CTkLabel(
                view_urgents_frame,
                font=('Terminal', 20),
            )
            task_label.configure(
                    text_color='red',
                    text = f"[{i}] - Course Name: {task['course']}\n\nTask Name: {task['task']}\n\nPriority Rating: {task['priority']}\n\nLevel of Difficulty: {task['difficulty']}\n\nDue Date: {task['due_date']}\n"
                )
            task_label.pack(
                pady=10
            )
    else:
        task_label=ctk.CTkLabel(
            view_urgents_frame,
            text="No incomplete tasks found!",
            font=("Terminal", 35, "bold")
        )
        task_label.pack(
            pady=200
        )
    inner_quit_button = ctk.CTkButton(
        aa_app,
        text="Cancel",
        font=('Terminal', 15),
        command= lambda: back_to_menu(view_urgents_frame, inner_quit_button)
    )  
    view_urgents_frame.pack(
        pady=25,
        padx=150,
        fill ='both', 
        expand = 1
    )

    button_or_label.destroy()
    inner_quit_button.pack(
        pady=10
    )

#study plan function
def study_plan_gui(frame, button_or_label):
    aa_app.geometry('900x800')


    frame.destroy()
    study_plan_frame = ctk.CTkScrollableFrame(
        aa_app,
        bg_color='transparent',
        corner_radius=10
    )

    study_plan_label = ctk.CTkLabel(
        study_plan_frame,
        text='Study Plan',
        font=('Terminal', 25, 'bold')
    )

    if aa_logic.check_incomp_tasks(tasks):
        sorted_tasks =  (aa_logic.urgent_sort(tasks))


        #quit button back to menu
    inner_quit_button = ctk.CTkButton(
        aa_app,
        text="Cancel",
        font=('Terminal', 15),
        command= lambda: back_to_menu(study_plan_frame, inner_quit_button)
    )
    

    
    study_plan_frame.pack(
        pady=25,
        padx=150,
        fill ='both', 
        expand = 1
    )
    study_plan_label.pack(
        pady=5
    )

    button_or_label.destroy()
    inner_quit_button.pack(
        pady=10
    )    

#mark as completed function
def mark_completed_gui(frame, button_or_label):
    aa_app.geometry('900x800')


    frame.destroy()
    mark_completed_frame = ctk.CTkScrollableFrame(
        aa_app,
        bg_color='transparent',
        corner_radius=10
    )

        #quit button back to menu
    inner_quit_button = ctk.CTkButton(
        aa_app,
        text="Cancel",
        font=('Terminal', 15),
        command= lambda: back_to_menu(mark_completed_frame, inner_quit_button)
    )
    

    
    mark_completed_frame.pack(
        pady=25,
        padx=150,
        fill ='both', 
        expand = 1
    )

    button_or_label.destroy()
    inner_quit_button.pack(
        pady=10
    )

#back/quit button functions
def back_to_menu(frame, button_or_label):
    frame.pack_forget()
    frame.destroy()
    button_or_label.destroy()
    aa_app.geometry('800x600')
    menu_screen()
def back_to_login(frame, quit):
    frame.destroy()
    quit.destroy()
    aa_app.geometry('800x600')      
    login_screen()

#helper method for empty values
def check_not_empty_gui(course, task, hours):
    if aa_logic.is_not_empty(course) and aa_logic.is_not_empty(task) and aa_logic.is_not_empty(hours):
        return True
    return False

aa_title.pack(pady=30)
login_screen()
aa_app.mainloop()