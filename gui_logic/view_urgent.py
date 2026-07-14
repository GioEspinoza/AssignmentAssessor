import customtkinter as ctk
from backend import aa_logic, session
from database import task_queries
from gui_logic.navigation import back_to_menu

#display only incomplete tasks that are urgent in order of priority (overdue first, then by least amount of days left) and display if they are overdue or not. If there are no incomplete tasks, display that there are no incomplete tasks.
def view_urgents_gui(frame, button_or_label, aa_app, fonts):
    aa_app.geometry('900x800')
    tasks = task_queries.get_tasks(session.get_current_user_id())

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
                font=fonts["body"],
                text_color='white',
                    text = f"[{i}] - Course Name: {task['course']}\n\nTask Name: {task['task']}\n\nPriority Rating: {task['priority']}\n\nLevel of Difficulty: {task['difficulty']}\n\nDue Date: {task['due_date']}\n"
                )
                task_label.pack(
                    pady=10
                )
            else:
                task_label=ctk.CTkLabel(
                    view_urgents_frame,
                    font=fonts["body"],
                    text_color='red',
                    text=f"[{i}] - Course Name: {task['course']}\n\nTask Name: {task['task']}\n\nLevel of Difficulty: {task['difficulty']}\n\nDue Date: OVERDUE\n\n"
                )
                task_label.pack(
                    pady=10
                )
    else:
        task_label=ctk.CTkLabel(
            view_urgents_frame,
            font=fonts["section_title"],
            text_color='white',
            text="No incomplete tasks found!",
            
        )
        task_label.pack(
            pady=200
        )
    inner_quit_button = ctk.CTkButton(
        aa_app,
        text="Cancel",
        font=fonts["button"],
        command= lambda: back_to_menu(aa_app, view_urgents_frame, inner_quit_button, fonts)
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
