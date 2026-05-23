from backend import storage, aa_logic
import customtkinter as ctk
from gui_logic.log_in import login_screen

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
    
    edit_task_button = ctk.CTkButton(
        menu_frame,
        font=('Terminal', 20),
        text="Edit Task",
        command= lambda: edit_task_gui(menu_frame, quit_button)
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
    edit_task_button.pack(
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
def view_tasks_gui(frame, button_or_label):
    aa_app.geometry('900x800')
    tasks = storage.load_data()

    frame.destroy()
    view_tasks_frame = ctk.CTkScrollableFrame(
        aa_app,
        bg_color='transparent',
        corner_radius=10
    )
    if tasks:
        sorted_tasks = aa_logic.alphabetical_tasks(tasks)
        for i, task in enumerate(sorted_tasks, start=1):
            task_label= ctk.CTkLabel(
                view_tasks_frame,
                font=('Terminal', 20),
            )
        
            if task['completed'] is False:
                if aa_logic.days_left(task["due_date"]) > 0:
                    task_label.configure(
                        text_color='white',
                        text = f"[{i}] - Course Name: {task['course']}\n\nTask Name: {task['task']}\n\nCompletion Status: Not Completed\n\nLevel of Difficulty: {task['difficulty']}\n\nDue Date: {task['due_date']}\n"
                    )
                    task_label.pack(
                        pady=10
                    )
                else:
                    task_label.configure(
                        text_color='red',
                        text=f"[{i}] - Course Name: {task['course']}\n\nTask Name: {task['task']}\n\nLevel of Difficulty: {task['difficulty']}\n\nDue Date: OVERDUE\n\n"
                    )
                    task_label.pack(
                        pady=10
                    )
            else:
                task_label.configure(
                    text_color='white',
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

#display only incomplete tasks that are urgent in order of priority (overdue first, then by least amount of days left) and display if they are overdue or not. If there are no incomplete tasks, display that there are no incomplete tasks.
def view_urgents_gui(frame, button_or_label):
    aa_app.geometry('900x800')
    tasks = storage.load_data()

    frame.destroy()
    view_urgents_frame = ctk.CTkScrollableFrame(
        aa_app,
        bg_color='transparent',
        corner_radius=10
    )
    if aa_logic.check_incomp_tasks(tasks):
        sorted_urgent_tasks = aa_logic.urgent_sort(tasks)

        #sorted_overdue_tasks = [task for task in aa_logic.urgent_sort(tasks) if aa_logic.days_left(task["due_date"]) <= 0]
        #sorted_urgent_tasks = [task for task in aa_logic.urgent_sort(tasks) if aa_logic.days_left(task["due_date"]) > 0]

        for i, task in enumerate([task for task in sorted_urgent_tasks if aa_logic.days_left(task["due_date"]) <= 0] + [task for task in sorted_urgent_tasks if aa_logic.days_left(task["due_date"]) > 0], start=1):
            if aa_logic.days_left(task["due_date"]) > 0:
                task_label=ctk.CTkLabel(
                view_urgents_frame,
                font=('Terminal', 20),
                text_color='white',
                    text = f"[{i}] - Course Name: {task['course']}\n\nTask Name: {task['task']}\n\nPriority Rating: {task['priority']}\n\nLevel of Difficulty: {task['difficulty']}\n\nDue Date: {task['due_date']}\n"
                )
                task_label.pack(
                    pady=10
                )
            else:
                task_label=ctk.CTkLabel(
                    view_urgents_frame,
                    font=('Terminal', 20),
                    text_color='red',
                    text=f"[{i}] - Course Name: {task['course']}\n\nTask Name: {task['task']}\n\nLevel of Difficulty: {task['difficulty']}\n\nDue Date: OVERDUE\n\n"
                )
                task_label.pack(
                    pady=10
                )
    else:
        task_label=ctk.CTkLabel(
            view_urgents_frame,
            font=("Terminal", 35, "bold"),
            text_color='white',
            text="No incomplete tasks found!",
            
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
    tasks = storage.load_data()

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
        pady=20
    )

    if aa_logic.check_incomp_tasks(tasks):
        sorted_urgent_tasks = aa_logic.urgent_sort(tasks)

        #sorted_overdue_tasks = [task for task in aa_logic.urgent_sort(tasks) if aa_logic.days_left(task["due_date"]) <= 0]
        #sorted_urgent_tasks = [task for task in aa_logic.urgent_sort(tasks) if aa_logic.days_left(task["due_date"]) > 0]

        #sort task list to only include urgent sorts but have overdues at the top.
        for i, task in enumerate([task for task in sorted_urgent_tasks if aa_logic.days_left(task["due_date"]) <= 0] + [task for task in sorted_urgent_tasks if aa_logic.days_left(task["due_date"]) > 0], start=1):
            hours_day = aa_logic.hours_per_day(float(task["hours"]), float(aa_logic.days_left(task["due_date"])))
            if aa_logic.days_left(task["due_date"]) > 0:
                task_label=ctk.CTkLabel(
                study_plan_frame,
                font=('Terminal', 20),
                text_color='white',
                text = f"[{i}] - Course: {task['course']}\n\nTask: {task['task']}\n\nLevel of Difficulty: {task['difficulty']}\n\nAmount of Days Left: {aa_logic.days_left(task["due_date"])}\n\nSuggested Hours Per Day: {hours_day}\n\n"
                )
                task_label.pack(
                    pady=10
                )
            else:
                task_label=ctk.CTkLabel(
                    study_plan_frame,
                    font=('Terminal', 20),
                    text_color='red',
                    text=f"[{i}] - Course: {task['course']}\n\nTask: {task['task']}\n\nDifficulty: {task['difficulty']}\n\nDays left: OVERDUE\n\nHours per day: ASAP\n\n"
                )
                task_label.pack(
                    pady=10
                )
    else:
        task_label=ctk.CTkLabel(
            study_plan_frame,
            text="No incomplete tasks found!",
            font=("Terminal", 35, "bold")
        )
        task_label.pack(
            pady=200
        )
    
    button_or_label.destroy()
    inner_quit_button.pack(
        pady=10
    )    

#edit task function
def edit_task_gui(frame, button_or_label=None):
    aa_app.geometry('800x600')
    tasks = storage.load_data()

    if frame != aa_app:
        frame.destroy()

    #outter frame that will hold all task frames
    mark_completed_frame = ctk.CTkScrollableFrame(
        aa_app,
        bg_color='transparent'
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
        padx=100,
        fill ='both', 
        expand = 1
    )
    
    for i, task in enumerate(tasks, start=1): 

        #instantiate a frame for each task label and button to be formatted in
        inner_tasks_frame = ctk.CTkFrame(
            mark_completed_frame
        )
        inner_tasks_frame.pack(
        padx=20,
        pady=20,
        fill='x'
        )
        
        #instantiate task label and pack for the task details
        inner_task_label = ctk.CTkLabel(
            inner_tasks_frame,
            justify='left',
            anchor='w',
            font=('Terminal', 25),
            text=f"[{i}] {task['course']} - {task['task']}"
        )
        inner_task_label.pack(
            side="left",
            padx=10,
            fill='x',
            expand=True,
            anchor='w'
        )
        
        #instantiate edit button for each task
        inner_task_button = ctk.CTkButton(
            inner_tasks_frame,
            text="Edit",
            fg_color='#1f6aa5',
            font=('Terminal', 25),
            corner_radius=10,
            hover_color='white',
            command= lambda index=i-1, selected_task=task: edit_task_handle(selected_task, index, mark_completed_frame, inner_quit_button)
        )
        inner_task_button.pack(
            side="right",
            padx=10
        )
    if button_or_label:
        button_or_label.destroy()

    inner_quit_button.pack(
        pady=20
    )

#handle edit frame for selected task
def edit_task_handle(task, index, frame, quit_button):
    #clear previous frame
    aa_app.geometry('800x700')
    frame.pack_forget()
    frame.destroy()
    quit_button.destroy()

    #frame that will fold the task info
    edit_task_handle_frame = ctk.CTkFrame(
        aa_app,
        bg_color='transparent',
        corner_radius=15
    )
    edit_task_handle_frame.pack(
        pady=25,
        padx=150,
        fill ='both', 
        expand = 1
    )

    #all elements in grid for incomp task
    if task['completed'] is False:
        #course label with its entry following to edit
        course_name_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text="Course Name:",
            font=('Terminal', 20)
        )
        course_name_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        course_name_entry=ctk.CTkEntry(
            edit_task_handle_frame,
            font=('Terminal', 20),
            placeholder_text=f"{task['course']}"
        )
        course_name_entry.grid(row=0, column=1, padx=20, pady=20)
        
        #task label with its entry following to edit
        task_name_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text="Task Name:",
            font=('Terminal', 20)
        )
        task_name_label.grid(row=1, column=0, padx=20, pady=20, sticky="w")
        
        task_name_entry=ctk.CTkEntry(
            edit_task_handle_frame,
            font=('Terminal', 20),
            placeholder_text=f"{task['task']}"
        )
        task_name_entry.grid(row=1, column=1, padx=20, pady=20)
        

        #completion label with its entry following to edit
        completion_status_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text="Completion Status:",
            font=('Terminal', 20)
        )
        completion_status_label.grid(row=2, column=0, padx=20, pady=20, sticky="w")

        completion_status_check = ctk.CTkCheckBox(
            edit_task_handle_frame,
            text=f"{task['completed']}", 
            command=lambda: update_checkbox_text(completion_status_check),
            onvalue="True", 
            offvalue="False"
        )
        completion_status_check.deselect()
        completion_status_check.grid(row=2, column=1, padx=20, pady=20)

        #difficulty label with its entry following to edit
        difficulty_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text=f"Difficulty: {task['difficulty']}",
            font=('Terminal', 20)
        )
        difficulty_label.grid(row=3, column=0, padx=20, pady=20, sticky="w")
        
        difficulty_slider=ctk.CTkSlider(
            edit_task_handle_frame,
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
        difficulty_slider.set(task['difficulty'])
        difficulty_slider.grid(row=3, column=1, padx=20, pady=20)

        #hours label with its prefilled entry to edit
        hours_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text="Hours Needed:",
            font=('Terminal', 20)
        )
        hours_label.grid(row=4, column=0, padx=20, pady=20, sticky="w")
        
        hours_entry=ctk.CTkEntry(
            edit_task_handle_frame,
            font=('Terminal', 20),
            placeholder_text=f"{task['hours']}"
        )
        hours_entry.grid(row=4, column=1, padx=20, pady=20)


        date_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text=f"Due Date:",
            font=('Terminal', 20)
        )
        date_label.grid(row=5, column=0, padx=20, pady=20, sticky="w")

        date_entry=ctk.CTkEntry(
            edit_task_handle_frame,
            font=('Terminal', 20),
            placeholder_text=f"{task['due_date']}"
        )
        date_entry.grid(row=5, column=1, padx=20, pady=20)

        #frame to hold three buttons at the bottom of the edit page, save, delete, and cancel
        button_frame = ctk.CTkFrame(
            edit_task_handle_frame,
            fg_color='transparent'
        )
        button_frame.grid(row=6, column=0, columnspan=2, rowspan=1, sticky="ew", padx=20, pady=20)

        #save button that will update task in tasks
        save_button = ctk.CTkButton(
            button_frame,
            text="Save Changes",
            font=('Terminal', 15),
            command= lambda: save_task_handle(
                index,
                completion_status_check.get() == "True",
                course_name_entry.get().strip(),
                task_name_entry.get().strip(),
                int(difficulty_slider.get()),            
                hours_entry.get(),
                date_entry.get(),
                edit_task_handle_frame,
                button_frame
            )
        )
        save_button.pack(
            side='left',
            padx=10,
            pady=10
        )

        #delete button that will delete task from tasks and update storage
        delete_button = ctk.CTkButton(
            button_frame,
            text="Delete Task",
            font=('Terminal', 15),
            command= lambda: delete_task_handle(
                index,
                edit_task_handle_frame,
                button_frame
            )
        )
        delete_button.pack(
            side='left',
            padx=10,
            pady=10
        )
        
        #cancel button that will take user back to menu without saving changes
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=('Terminal', 15),
            command= lambda: back_to_edit_task_gui(edit_task_handle_frame)
        )
        cancel_button.pack(
            side='left',
            padx=10,
            pady=10
        )

    #elements in grid for comp tasks
    else:
        #label with its entry following to edit
        course_name_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text="Course Name:",
            font=('Terminal', 20)
        )
        course_name_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        course_name_entry=ctk.CTkEntry(
            edit_task_handle_frame,
            font=('Terminal', 20),
            placeholder_text=f"{task['course']}"
        )
        course_name_entry.grid(row=0, column=1, padx=20, pady=20)
        
        task_name_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text="Task Name:",
            font=('Terminal', 20)
        )
        task_name_label.grid(row=1, column=0, padx=20, pady=20, sticky="w")
        
        task_name_entry=ctk.CTkEntry(
            edit_task_handle_frame,
            font=('Terminal', 20),
            placeholder_text=f"{task['task']}"
        )
        task_name_entry.grid(row=1, column=1, padx=20, pady=20)

        completion_status_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text="Completion Status:",
            font=('Terminal', 20)
        )
        completion_status_label.grid(row=2, column=0, padx=20, pady=20, sticky="w")

        completion_status_check = ctk.CTkCheckBox(
            edit_task_handle_frame,
            text=f"{task['completed']}", 
            command=lambda: update_checkbox_text(completion_status_check),
            onvalue="True", 
            offvalue="False"
        )
        completion_status_check.select()
        completion_status_check.grid(row=2, column=1, padx=20, pady=20)

        difficulty_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text=f"Difficulty: {task['difficulty']}",
            font=('Terminal', 20)
        )
        difficulty_label.grid(row=3, column=0, padx=20, pady=20, sticky="w")
        
        difficulty_slider=ctk.CTkSlider(
            edit_task_handle_frame,
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
        difficulty_slider.set(task['difficulty'])
        difficulty_slider.grid(row=3, column=1, padx=20, pady=20)


        hours_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text=f"Hours Used: {task['hours']}",
            font=('Terminal', 20)
        )
        hours_label.grid(row=4, column=0, padx=20, pady=20, sticky="w")

        hours_entry=ctk.CTkEntry(
            edit_task_handle_frame,
            font=('Terminal', 20),
            placeholder_text=f"{task['hours']}"
        )
        hours_entry.grid(row=4, column=1, padx=20, pady=20)
        
        date_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text=f"Date Completed: {task['date_completed']}",
            font=('Terminal', 20)
        )
        date_label.grid(row=5, column=0, padx=20, pady=20, sticky="w")

        date_entry=ctk.CTkEntry(
            edit_task_handle_frame,
            font=('Terminal', 20),
            placeholder_text=f"{task['date_completed']}"
        )
        date_entry.grid(row=5, column=1, padx=20, pady=20)

        #frame to hold three buttons at the bottom of the edit page, save, delete, and cancel
        button_frame = ctk.CTkFrame(
            edit_task_handle_frame,
            fg_color='transparent'
        )
        button_frame.grid(row=6, column=0, columnspan=2, rowspan=1, sticky="ew", padx=20, pady=20)

        #save button that will update task in tasks
        save_button = ctk.CTkButton(
            button_frame,
            text="Save Changes",
            font=('Terminal', 15),
            command= lambda: save_task_handle(
                index,
                completion_status_check.get() == "True",
                course_name_entry.get().strip(),
                task_name_entry.get().strip(),
                int(difficulty_slider.get()),            
                hours_entry.get(),
                date_entry.get(),
                edit_task_handle_frame,
                button_frame
            )
        )
        save_button.pack(
            side='left',
            padx=10,
            pady=10
        )

        #delete button that will delete task from tasks and update storage
        delete_button = ctk.CTkButton(
            button_frame,
            text="Delete Task",
            font=('Terminal', 15),
            command= lambda: delete_task_handle(
                index,
                edit_task_handle_frame,
                button_frame
            )
        )
        delete_button.pack(
            side='left',
            padx=10,
            pady=10
        )
        
        #cancel button that will take user back to menu without saving changes
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=('Terminal', 15),
            command= lambda: back_to_edit_task_gui(edit_task_handle_frame)
        )
        cancel_button.pack(
            side='left',
            padx=10,
            pady=10
        )

#helper function to update checkbox text on click
def update_checkbox_text(checkbox):
    # Retrieve current value (onvalue/offvalue) and update text
    checkbox.configure(
        font=('Terminal', 20),
        text=f"{checkbox.get()}")

#handle save button for edits
def save_task_handle(index, is_comp, course, task, difficulty, hours, date, frame, button_or_label):
    tasks = storage.load_data()
    if check_not_empty_gui(course, task, hours) is False:
        invalid_label = ctk.CTkLabel(
            aa_app,
            font=('Terminal', 20),
            bg_color='transparent',
            text_color='red',
            text='Empty inputs detected!'        
        )
        invalid_label.pack(
            pady=5
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return
    
    if aa_logic.is_hours(hours) is False:
        invalid_label = ctk.CTkLabel(
            aa_app,
            font=('Terminal', 20),
            bg_color='transparent',
            text_color='red',
            text='Invalid hour input!'        
        )
        invalid_label.pack(
            pady=5
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return
    
    if is_comp is False and aa_logic.valid_due_date(date) is False:
        invalid_label = ctk.CTkLabel(
            aa_app,
            font=('Terminal', 20),
            bg_color='transparent',
            text_color='red',
            text='Invalid date input - (MM-DD-YYYY)!'        
        )
        invalid_label.pack(
            pady=5
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return
    
    if is_comp is True and aa_logic.valid_comp_date(date) is False:
        invalid_label = ctk.CTkLabel(
            aa_app,
            font=('Terminal', 20),
            bg_color='transparent',
            text_color='red',
            text='Invalid date input - (MM-DD-YYYY)!'        
        )
        invalid_label.pack(
            pady=5
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return

    updated_task = {
        "course": course,
        "task": task,
        "completed": is_comp,
        "difficulty": difficulty,
        "hours": hours,
        "due_date": date if not is_comp else None,
        "date_completed": date if is_comp else None
    }
    tasks[index] = updated_task
    storage.save_data(tasks)
    edit_task_gui(frame, button_or_label)

#handle delete button for edits with confirmation popup
def delete_task_handle(index, frame, button_or_label):
    frame.pack_forget()
    #popup window to confirm delete
    confirm_frame = ctk.CTkFrame(aa_app)
    confirm_frame.pack(
        pady=100,  
        padx=200,
        fill='both',
        expand=1
    )
    confirm_label = ctk.CTkLabel(
        confirm_frame,
        text="Are you sure you want to delete this task?",
        font=('Terminal', 15)
    )
    confirm_label.pack(
        pady=20
    )

    button_frame = ctk.CTkFrame(
        confirm_frame,
        bg_color='transparent',
        fg_color='transparent'
    )
    button_frame.pack(
        pady=20
    )

    yes_button = ctk.CTkButton(
        button_frame,
        text="Yes",
        font=('Terminal', 15),
        fg_color='red',
        hover_color='white',
        command=lambda: confirm_delete(index, confirm_frame, frame, button_or_label)
    )
    yes_button.pack(
        side='left',
        padx=10
    )

    no_button = ctk.CTkButton(
        button_frame,
        text="No",
        font=('Terminal', 15),
        command=lambda: cancel_delete(frame, confirm_frame, button_or_label)
    )
    no_button.pack(
        side='left',
        padx=10
    )

#confirm delete function to delete task and update storage
def confirm_delete(index, confirm_frame, frame, button_or_label):
    tasks = storage.load_data()
    del tasks[index]
    storage.save_data(tasks)
    confirm_frame.destroy()
    edit_task_gui(frame, button_or_label)
def cancel_delete(frame, confirm_frame, button_or_label):
    confirm_frame.destroy()
    frame.pack(
        pady=25,
        padx=150,
        fill ='both', 
        expand = 1
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
    login_screen(aa_app, aa_title, menu_screen)
def back_to_edit_task_gui(frame):
    frame.pack_forget()
    frame.destroy()
    aa_app.geometry('800x700')
    edit_task_gui(aa_app)

#helper method for empty values
def check_not_empty_gui(course, task, hours):
    if aa_logic.is_not_empty(course) and aa_logic.is_not_empty(task) and aa_logic.is_not_empty(hours):
        return True
    return False

aa_title.pack(pady=30)
login_screen(aa_app, aa_title, menu_screen)
aa_app.mainloop()