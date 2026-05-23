import customtkinter as ctk
from aa_gui import back_to_menu
from backend import storage
from backend import aa_logic

#study plan function
def study_plan_gui(frame, button_or_label, aa_app): 
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