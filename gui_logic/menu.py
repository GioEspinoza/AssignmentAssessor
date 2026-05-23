import customtkinter as ctk
from aa_gui import back_to_login
from backend import storage
from gui_logic import add_task
#will show menu after authencation
def menu_screen(aa_app):

    tasks = storage.load_data()
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
        command= lambda: add_task.add_task_gui(menu_frame, quit_button, aa_app)
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