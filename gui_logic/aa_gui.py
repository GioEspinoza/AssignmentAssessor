import sys
from pathlib import Path
from backend import storage, auth, aa_logic
import customtkinter as ctk

user_data = storage.load_user_prof()


def new_user():
    while True:
        if aa_logic.check_new_name(username_entry.get()):
            if aa_logic.check_new_pass(password_entry.get()):
                storage.save_user_prof(username_entry.get(),auth.hash_password(password_entry.get()))
                return username_entry.get()
            else:
                continue
        else:
            continue

def log_in():
    ...

def show_menu():
    ...

aa_app = ctk.CTk()
#set title and window size
aa_app.title('Assignment Assessor')
aa_app.geometry('800x600')

#set title text
aa_title = ctk.CTkLabel(
    aa_app, 
    pady=25,
    text='Assignment Assessor',
    font=('Terminal',50))

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

#instantiate buttons for register and log in
log_in_button = ctk.CTkButton(
    authentication_frame,
    corner_radius=15,
    text='Log in',
    font=("Terminal", 20)
)

register_button = ctk.CTkButton(
    authentication_frame,
    corner_radius=15,
    text= 'Register',
    font=("Terminal", 20)
    )

#if user data is none, set up registration page
if user_data is None:
    aa_subtitle.configure(
        text='Welcome new User! Please register',
        font=('Terminal',25))
    
    
    
    username_entry.pack(
        pady=30
    )
    password_entry.pack(
        pady=30    
    )

    register_button.pack(
        pady=40
    )

#if user has data, set up log in page
else:
    aa_subtitle.configure(
        text=f"Welcome {user_data.get('username')}, Please log in",
        font=('Terminal',25)
    )

    password_entry.pack(
        pady=40
    )

    log_in_button.pack(
        pady=50
    )

aa_title.pack(pady=30)
aa_subtitle.pack(pady=10)
authentication_frame.pack(pady=20, expand=True)
authentication_frame.pack_propagate(False)

aa_app.mainloop()
