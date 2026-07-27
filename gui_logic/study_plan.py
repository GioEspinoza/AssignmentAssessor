import customtkinter as ctk
from database import task_queries
from backend import session, task_rules, validation
from gui_logic.navigation import back_to_menu

#study plan function
def study_plan_gui(frame, button_or_label, aa_app, fonts): 
    aa_app.geometry('900x800')
    tasks = task_queries.get_tasks(session.get_current_user_id())

    frame.destroy()
    study_plan_frame = ctk.CTkScrollableFrame(
        aa_app,
        bg_color='transparent',
        corner_radius=10
    )

    study_plan_label = ctk.CTkLabel(
        study_plan_frame,
        text='Study Plan',
        font=fonts["page_title"]
    )

    #quit button back to menu
    inner_quit_button = ctk.CTkButton(
        aa_app,
        text="Cancel",
        font=fonts["button"],
        command= lambda: back_to_menu(aa_app, study_plan_frame, inner_quit_button, fonts)
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

    if task_rules.check_incomp_tasks(tasks):
        sorted_urgent_tasks = task_rules.urgent_sort(tasks)

        #sort task list to only include urgent sorts but have overdues at the top.
        for i, task in enumerate([task for task in sorted_urgent_tasks if validation.days_left(task["due_date"]) <= 0] + [task for task in sorted_urgent_tasks if validation.days_left(task["due_date"]) > 0], start=1):
            hours_day = task_rules.hours_per_day(
                task_rules.remaining_hours(task),
                float(validation.days_left(task["due_date"]))
            )
            if validation.days_left(task["due_date"]) > 0:
                task_label=ctk.CTkLabel(
                study_plan_frame,
                font=fonts["body"],
                text_color='white',
                text = f"[{i}] - Course: {task['course']}\n\nTask: {task['task']}\n\nLevel of Difficulty: {task['difficulty']}\n\nAmount of Days Left: {validation.days_left(task["due_date"])}\n\nSuggested Hours Per Day: {hours_day}\n\n"
                )
                task_label.pack(
                    pady=10
                )
            else:
                task_label=ctk.CTkLabel(
                    study_plan_frame,
                    font=fonts["body"],
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
            font=fonts["section_title"]
        )
        task_label.pack(
            pady=200
        )
    
    button_or_label.destroy()
    inner_quit_button.pack(
        pady=10
    )  
