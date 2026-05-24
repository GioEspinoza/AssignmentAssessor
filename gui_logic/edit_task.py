import customtkinter as ctk
from backend import storage
from backend import aa_logic
from gui_logic.navigation import back_to_menu, check_not_empty_gui, update_checkbox_text


#edit task function
def edit_task_gui(frame, button_or_label=None, aa_app=None):
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
        command= lambda: back_to_menu(aa_app, mark_completed_frame, inner_quit_button)
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
            command= lambda index=i-1, selected_task=task: edit_task_handle(selected_task, index, mark_completed_frame, inner_quit_button, aa_app)
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
def edit_task_handle(task, index, frame, quit_button, aa_app):
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
                aa_app
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
                button_frame,
                aa_app
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
            command= lambda: back_to_edit_task_gui(edit_task_handle_frame, aa_app)
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
                aa_app
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
                button_frame,
                aa_app
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
            command= lambda: back_to_edit_task_gui(edit_task_handle_frame, aa_app)
        )
        cancel_button.pack(
            side='left',
            padx=10,
            pady=10
        )

#handle save button for edits
def save_task_handle(index, is_comp, course, task, difficulty, hours, date, frame, aa_app):
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
    back_to_edit_task_gui(frame, aa_app)

#handle delete button for edits with confirmation popup
def delete_task_handle(index, frame, button_or_label, aa_app):
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
        command=lambda: confirm_delete(index, confirm_frame, frame, aa_app)
    )
    yes_button.pack(
        side='left',
        padx=10
    )

    no_button = ctk.CTkButton(
        button_frame,
        text="No",
        font=('Terminal', 15),
        command=lambda: cancel_delete(frame, confirm_frame)
    )
    no_button.pack(
        side='left',
        padx=10
    )


#confirm delete function to delete task and update storage
def confirm_delete(index, confirm_frame, frame, aa_app):
    tasks = storage.load_data()
    del tasks[index]
    storage.save_data(tasks)
    confirm_frame.destroy()
    back_to_edit_task_gui(frame, aa_app)
def cancel_delete(frame, confirm_frame):
    confirm_frame.destroy()
    frame.pack(
        pady=25,
        padx=150,
        fill ='both', 
        expand = 1
    )

def back_to_edit_task_gui(frame, aa_app):
    frame.pack_forget()
    frame.destroy()
    aa_app.geometry('800x700')
    edit_task_gui(aa_app, aa_app=aa_app)
    
