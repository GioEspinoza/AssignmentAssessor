import customtkinter as ctk 
from backend import storage
from backend import aa_logic
from gui_logic.navigation import back_to_menu

#view task function
def view_tasks_gui(frame, button_or_label, aa_app):
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
        command= lambda: back_to_menu(aa_app, view_tasks_frame, inner_quit_button)
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
