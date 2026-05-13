#import sys
#from pathlib import Path
from backend import storage, auth, aa_logic
import customtkinter as ctk

user_data = storage.load_user_prof()

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

#encapsulate login screen
def login_screen():
    #instantiate welcoming substitute
    aa_subtitle = ctk.CTkLabel(aa_app)

    #instatiante authentication frame
    authentication_frame = ctk.CTkFrame(
        aa_app, 
        width=400, 
        height=300,
        corner_radius=15
    )

    #instantiate and configure username and password text boxes
    password_entry = ctk.CTkEntry(
        authentication_frame
    )
    password_entry.configure(
            placeholder_text="Password",
            placeholder_text_color='grey',
            font=('Terminal', 15),
            show="*"
        )

    username_entry = ctk.CTkEntry(
        authentication_frame
    )
    username_entry.configure(
        placeholder_text='Username',
        placeholder_text_color='grey',
        font=('Terminal', 15)
    )

    #instantiate label for invalid password/usernames
    invalid_label = ctk.CTkLabel(
            authentication_frame,
            font=('Terminal', 15),
            bg_color='transparent',
            text_color='red',
            text=''        
        )

    #instantiate buttons for register and log in
    log_in_button = ctk.CTkButton(
        authentication_frame,
        corner_radius=10,
        text='Log in',
        font=("Terminal", 25),
        command = lambda: log_in(
            password_entry.get(),
            invalid_label,
            authentication_frame,
            aa_subtitle
        )
    )

    register_button = ctk.CTkButton(
        authentication_frame,
        corner_radius=20,
        text= 'Register',
        font=("Terminal", 25),
        command= lambda: new_user(
            username_entry.get(),
            password_entry.get(),
            invalid_label,
            authentication_frame,
            aa_subtitle
        )
        )

    #if user data is none, set up registration page
    if user_data is None:
        aa_subtitle.configure(
            text='Welcome new User! Please register',
            font=('Terminal',25))
        aa_subtitle.pack(pady=10)

        username_entry.pack(
            pady=20
        )
        password_entry.pack(
            pady=10    
        )
        register_button.pack(
            pady=30
        )

    #if user has data, set up log in page
    else:
        aa_subtitle.configure(
            text=f"Welcome {user_data.get('username')}, Please log in",
            font=('Terminal',25)
        )
        aa_subtitle.pack(pady=10)

        password_entry.pack(
            pady=70
        )

        log_in_button.pack(
            pady=20
        )
    authentication_frame.pack(pady=20, expand=True)
    authentication_frame.pack_propagate(False)
    
#function that will register new user
def new_user(username_entry, password_entry, invalid_label, authentication_frame, aa_subtitle):
    global user_data
    #check if user and password are valid
    valid, message = auth.check_new_name(username_entry)
    passvalid, passmessage = auth.check_new_pass(password_entry)
    
    if not valid:
        #if not refresh label for invalid inputs
        invalid_label.configure(
            text=message
        )
        invalid_label.pack(
            pady=10
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return
    
    if not passvalid:
        #if not refresh label for invalid inputs
        invalid_label.configure(
            text=passmessage
        )
        invalid_label.pack(
            pady=10
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return
        
    storage.save_user_prof(
            username_entry,
            auth.hash_password(password_entry)
            )
    authentication_frame.destroy()
    aa_title.pack_forget()
    aa_subtitle.pack_forget()
    menu_screen()
                
#function that will authenticate old user
def log_in(password_entry, invalid_label, authentication_frame, aa_subtitle):
    #load in saved password
    if not auth.check_hpassword(user_data.get('hpassword'), password_entry):
        #if not refresh label for invalid inputs
        invalid_label.configure(
            text="Incorrect password"
         )
        invalid_label.pack(
            pady=10
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return
    
    authentication_frame.destroy()
    aa_title.configure(
        font=("Terminal", 40),
        pady=5
    )
    aa_subtitle.pack_forget()
    menu_screen()

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
        text="View Task(s)"
        )
    
    view_urgent_button = ctk.CTkButton(
        menu_frame,
        font=('Terminal', 20),
        text="View Urgent(s)"
        )
    
    study_button = ctk.CTkButton(
        menu_frame,
        font=('Terminal', 20),
        text="Study Plan"
        )
    
    completed_button = ctk.CTkButton(
        menu_frame,
        font=('Terminal', 20),
        text="Mark as Complete"
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

    completed_button.pack(
        pady=25
    )
    
    #pack exit button
    quit_button.pack(
        pady=10
    )

#add task function
def add_task_gui(menu_frame, quit_button):
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
        placeholder_text_color='grey',
        font=('Terminal', 15)
    )

    task_entry = ctk.CTkEntry(
        add_task_frame,
        placeholder_text='Task Name',
        placeholder_text_color='grey',
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

    #instatiate difficulty label and scale
    difficulty_label = ctk.CTkLabel(
        add_task_frame,
        text="On a scale of 1-5, how difficult?",
        font=("Terminal", 10)
    )

    difficulty_scale = ctk.CTkSlider(
        add_task_frame,
        corner_radius=10,
        button_color='white',
        button_hover_color='grey',
        button_corner_radius=10,
        border_color='transparent',
        number_of_steps=4,
        progress_color='red',
    )

    #quit button back to menu
    inner_quit_button = ctk.CTkButton(
        aa_app,
        text="Cancel",
        font=('Terminal', 15),
        command= lambda: back_to_menu(add_task_frame, inner_quit_button)
    )
    #unshow menu frame and then show task frame
    menu_frame.destroy()
    add_task_frame.pack(
        pady=20,
        padx=200,
        fill ='both', 
        expand = 1
    )
    
    #show task frame inputs
    course_entry.pack(
        pady=10
    )
    task_entry.pack(
        pady=10
    )
    completed_box.pack(
        pady=10
    )
    difficulty_label.pack(
        pady=15
    )
    difficulty_scale.pack(
    )

    #destroy outer quit button and show inner quit button
    quit_button.destroy()
    inner_quit_button.pack(
        pady=10
    )

def back_to_menu(frame, inner_quit):
    frame.destroy()
    inner_quit.destroy()
    menu_screen()

def back_to_login(frame, quit):
    frame.destroy()
    quit.destroy()
    login_screen()

aa_title.pack(pady=30)
login_screen()
aa_app.mainloop()