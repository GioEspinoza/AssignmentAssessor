from backend import storage, aa_logic
import customtkinter as ctk
from gui_logic.edit_task import edit_task_gui
from gui_logic.log_in import login_screen
from gui_logic.menu import menu_screen

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

#helper function to update checkbox text on click
def update_checkbox_text(checkbox):
    # Retrieve current value (onvalue/offvalue) and update text
    checkbox.configure(
        font=('Terminal', 20),
        text=f"{checkbox.get()}")

#helper method for empty values
def check_not_empty_gui(course, task, hours):
    if aa_logic.is_not_empty(course) and aa_logic.is_not_empty(task) and aa_logic.is_not_empty(hours):
        return True
    return False

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
    
aa_title.pack(pady=30)
login_screen(aa_app, aa_title, menu_screen)
aa_app.mainloop()