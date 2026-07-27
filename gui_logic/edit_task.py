import customtkinter as ctk
from database import task_queries
from backend import session, validation
from gui_logic.navigation import back_to_menu, check_not_empty_gui


STATUS_VALUES = {
    "Not Started": "not_started",
    "In Progress": "in_progress",
    "Completed": "completed",
}

#edit task function
def edit_task_gui(frame, aa_app, fonts, button_or_label=None):
    aa_app.geometry('800x600')

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
        font=fonts["button"],
        command= lambda: back_to_menu(aa_app, mark_completed_frame, inner_quit_button, fonts)
    )
    
    mark_completed_frame.pack(
        pady=25,
        padx=100,
        fill ='both', 
        expand = 1
    )
    
    if task_queries.get_tasks(session.get_current_user_id()):
        for i, task in enumerate(task_queries.get_tasks(session.get_current_user_id()), start=1): 

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
                font=fonts["card_title"],
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
                font=fonts["button"],
                corner_radius=10,
                hover_color='white',
                command= lambda selected_task=task: edit_task_handle(selected_task, mark_completed_frame, inner_quit_button, aa_app, fonts)
            )
            inner_task_button.pack(
                side="right",
                padx=10
            )
    else:
        task_label=ctk.CTkLabel(
            mark_completed_frame,
            text="No tasks found!",
            font=fonts["section_title"]
        )
        task_label.pack(
            pady=200
        )
    if button_or_label:
        button_or_label.destroy()

    inner_quit_button.pack(
        pady=20
    )

#handle edit frame for selected task
def edit_task_handle(task, frame, quit_button, aa_app, fonts):
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
    if task['status'] != "completed":
        #course label with its entry following to edit
        course_name_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text="Course Name:",
            font=fonts["body_bold"]
        )
        course_name_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        course_name_entry=ctk.CTkEntry(
            edit_task_handle_frame,
            font=fonts["input"],
            placeholder_text=f"{task['course']}"
        )
        course_name_entry.grid(row=0, column=1, padx=20, pady=20)
        
        #task label with its entry following to edit
        task_name_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text="Task Name:",
            font=fonts["body_bold"]
        )
        task_name_label.grid(row=1, column=0, padx=20, pady=20, sticky="w")
        
        task_name_entry=ctk.CTkEntry(
            edit_task_handle_frame,
            font=fonts["input"],
            placeholder_text=f"{task['task']}"
        )
        task_name_entry.grid(row=1, column=1, padx=20, pady=20)
        

        #completion label with its entry following to edit
        completion_status_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text="Completion Status:",
            font=fonts["body_bold"]
        )
        completion_status_label.grid(row=2, column=0, padx=20, pady=20, sticky="w")

        completion_status_check = ctk.CTkSegmentedButton(
            edit_task_handle_frame,
            values=list(STATUS_VALUES),
            font=fonts["body"],
        )
        completion_status_check.set(
            task['status'].replace('_', ' ').title()
        )
        completion_status_check.grid(row=2, column=1, padx=20, pady=20)

        #difficulty label with its entry following to edit
        difficulty_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text=f"Difficulty: {task['difficulty']}",
            font=fonts["body_bold"]
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
            font=fonts["body_bold"]
        )
        hours_label.grid(row=4, column=0, padx=20, pady=20, sticky="w")
        
        hours_entry=ctk.CTkEntry(
            edit_task_handle_frame,
            font=fonts["input"],
            placeholder_text=f"{task['estimated_hours']}"
        )
        hours_entry.grid(row=4, column=1, padx=20, pady=20)


        date_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text=f"Due Date:",
            font=fonts["body_bold"]
        )
        date_label.grid(row=5, column=0, padx=20, pady=20, sticky="w")

        date_entry=ctk.CTkEntry(
            edit_task_handle_frame,
            font=fonts["input"],
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
            font=fonts["button"],
            command= lambda: save_task_handle(
                task['task_id'],
                completion_status_check.get(),
                task['course_id'],
                course_name_entry.get().strip(),
                task_name_entry.get().strip(),
                int(difficulty_slider.get()),            
                hours_entry.get(),
                task.get('hours_used'),
                date_entry.get(),
                edit_task_handle_frame,
                aa_app,
                fonts
            )
        )
        save_button.pack(
            side='left',
            padx=10,
            pady=10
        )

        #delete button that will delete task from tasks and update database
        delete_button = ctk.CTkButton(
            button_frame,
            text="Delete Task",
            font=fonts["button"],
            command= lambda: delete_task_handle(
                task['task_id'],
                edit_task_handle_frame,
                button_frame,
                aa_app,
                fonts
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
            font=fonts["button"],
            command= lambda: back_to_edit_task_gui(edit_task_handle_frame, aa_app, fonts)
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
            font=fonts["body_bold"]
        )
        course_name_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        course_name_entry=ctk.CTkEntry(
            edit_task_handle_frame,
            font=fonts["input"],
            placeholder_text=f"{task['course']}"
        )
        course_name_entry.grid(row=0, column=1, padx=20, pady=20)
        
        task_name_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text="Task Name:",
            font=fonts["body_bold"]
        )
        task_name_label.grid(row=1, column=0, padx=20, pady=20, sticky="w")
        
        task_name_entry=ctk.CTkEntry(
            edit_task_handle_frame,
            font=fonts["input"],
            placeholder_text=f"{task['task']}"
        )
        task_name_entry.grid(row=1, column=1, padx=20, pady=20)

        completion_status_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text="Completion Status:",
            font=fonts["body_bold"]
        )
        completion_status_label.grid(row=2, column=0, padx=20, pady=20, sticky="w")

        completion_status_check = ctk.CTkSegmentedButton(
            edit_task_handle_frame,
            values=list(STATUS_VALUES),
            font=fonts["body"],
        )
        completion_status_check.set("Completed")
        completion_status_check.grid(row=2, column=1, padx=20, pady=20)

        difficulty_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text=f"Difficulty: {task['difficulty']}",
            font=fonts["body_bold"]
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
            text=f"Hours Used: {task['hours_used']}",
            font=fonts["body_bold"]
        )
        hours_label.grid(row=4, column=0, padx=20, pady=20, sticky="w")

        hours_entry=ctk.CTkEntry(
            edit_task_handle_frame,
            font=fonts["input"],
            placeholder_text=f"{task['hours_used']}"
        )
        hours_entry.grid(row=4, column=1, padx=20, pady=20)
        
        date_label=ctk.CTkLabel(
            edit_task_handle_frame,
            text=f"Date Completed: {task['date_completed']}",
            font=fonts["body_bold"]
        )
        date_label.grid(row=5, column=0, padx=20, pady=20, sticky="w")

        date_entry=ctk.CTkEntry(
            edit_task_handle_frame,
            font=fonts["input"],
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
            font=fonts["button"],
            command= lambda: save_task_handle(
                task['task_id'],
                completion_status_check.get(),
                task['course_id'],
                course_name_entry.get().strip(),
                task_name_entry.get().strip(),
                int(difficulty_slider.get()),            
                task.get('estimated_hours'),
                hours_entry.get(),
                date_entry.get(),
                edit_task_handle_frame,
                aa_app,
                fonts
            )
        )
        save_button.pack(
            side='left',
            padx=10,
            pady=10
        )

        #delete button that will delete task from tasks and update database
        delete_button = ctk.CTkButton(
            button_frame,
            text="Delete Task",
            font=fonts["button"],
            command= lambda: delete_task_handle(
                task['task_id'],
                edit_task_handle_frame,
                button_frame,
                aa_app,
                fonts
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
            font=fonts["button"],
            command= lambda: back_to_edit_task_gui(edit_task_handle_frame, aa_app, fonts)
        )
        cancel_button.pack(
            side='left',
            padx=10,
            pady=10
        )

#handle save button for edits
def save_task_handle(
    task_id,
    status_label,
    course_id,
    course,
    task,
    difficulty,
    estimated_hours,
    hours_used,
    date,
    frame,
    aa_app,
    fonts,
):
    tasks = task_queries.get_tasks(session.get_current_user_id())
    status = STATUS_VALUES[status_label]
    hours = hours_used if status == "completed" else estimated_hours

    if check_not_empty_gui(course, task, hours) is False:
        invalid_label = ctk.CTkLabel(
            aa_app,
            font=fonts["small_bold"],
            bg_color='transparent',
            text_color='red',
            text='Empty inputs detected!'        
        )
        invalid_label.pack(
            pady=5
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return
    
    if validation.is_hours(hours) is False:
        invalid_label = ctk.CTkLabel(
            aa_app,
            font=fonts["small_bold"],
            bg_color='transparent',
            text_color='red',
            text='Invalid hour input!'        
        )
        invalid_label.pack(
            pady=5
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return
    
    if status != "completed" and validation.valid_due_date(date) is False:
        invalid_label = ctk.CTkLabel(
            aa_app,
            font=fonts["small_bold"],
            bg_color='transparent',
            text_color='red',
            text='Invalid date input - (MM-DD-YYYY)!'        
        )
        invalid_label.pack(
            pady=5
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return
    
    if status == "completed" and validation.valid_comp_date(date) is False:
        invalid_label = ctk.CTkLabel(
            aa_app,
            font=fonts["small_bold"],
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
        "task_id": task_id,
        "course_id": course_id,
        "course": course,
        "task": task,
        "status": status,
        "difficulty": difficulty,
        "estimated_hours": estimated_hours,
        "hours_used": hours_used,
        "due_date": date if status != "completed" else None,
        "date_completed": date if status == "completed" else None
    }

    task_queries.update_task(task_id, updated_task)
    back_to_edit_task_gui(frame, aa_app, fonts)

#handle delete button for edits with confirmation popup
def delete_task_handle(task_id, frame, button_frame, aa_app, fonts):
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
        font=fonts["body"]
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
        font=fonts["button"],
        fg_color='red',
        hover_color='white',
        command=lambda: confirm_delete(task_id, confirm_frame, frame, aa_app, fonts)
    )
    yes_button.pack(
        side='left',
        padx=10
    )

    no_button = ctk.CTkButton(
        button_frame,
        text="No",
        font=fonts["button"],
        command=lambda: cancel_delete(frame, confirm_frame)
    )
    no_button.pack(
        side='left',
        padx=10
    )


#confirm delete function to delete task and update database
def confirm_delete(task_id, confirm_frame, frame, aa_app, fonts):
    task_queries.delete_task(task_id)
    confirm_frame.destroy()
    back_to_edit_task_gui(frame, aa_app, fonts)
def cancel_delete(frame, confirm_frame):
    confirm_frame.destroy()
    frame.pack(
        pady=25,
        padx=150,
        fill ='both', 
        expand = 1
    )

def back_to_edit_task_gui(frame, aa_app, fonts):
    frame.pack_forget()
    frame.destroy()
    aa_app.geometry('800x700')
    edit_task_gui(aa_app, aa_app=aa_app, fonts=fonts)
    
