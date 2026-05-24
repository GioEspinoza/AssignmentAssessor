import customtkinter as ctk
from backend import storage
from backend import aa_logic
from gui_logic.navigation import back_to_menu, check_not_empty_gui

#add task function
def add_task_gui(frame, button_or_label, aa_app):
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

    #instatiate difficulty label and slider
    difficulty_label = ctk.CTkLabel(
        add_task_frame,
        text="On a scale of 1-5, how difficult?",
        font=("Terminal", 15)
    )
    difficulty_slider = ctk.CTkSlider(
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
            int(difficulty_slider.get()),            
            hours_entry.get(),
            date_entry.get(),
            invalid_label,
            add_task_frame,
            inner_quit_button,
            aa_app
        )
    )
    #quit button back to menu
    inner_quit_button = ctk.CTkButton(
        add_task_frame,
        text="Cancel",
        font=('Terminal', 15),
        command= lambda: back_to_menu(aa_app, add_task_frame, inner_quit_button)
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
    difficulty_slider.pack(
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
def submit_task_handle(is_comp, course, task, difficulty, hours, date, invalid_label, frame, quit_button, aa_app):
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
        
        rev_task_gui(aa_logic.add_task(is_comp, course, task, difficulty, None, hours, None, date), frame, quit_button, aa_app)
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

    rev_task_gui(aa_logic.add_task(is_comp, course, task, difficulty, hours, None, date, None), frame, quit_button, aa_app)
    return
#review task logic for gui
def rev_task_gui(task, frame, quit_button, aa_app):
    tasks = storage.load_data()
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
        command= lambda: add_task_gui(rev_task_frame, task_recognized_label, aa_app)
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
    command= lambda: submit_task(tasks, task, rev_task_frame, task_recognized_label, aa_app)
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
def submit_task(tasks, task, frame, button_or_label, aa_app):
    tasks.append(task)
    storage.save_data(tasks)
    back_to_menu(aa_app, frame, button_or_label)
