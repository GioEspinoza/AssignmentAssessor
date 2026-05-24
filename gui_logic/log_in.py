#encapsulate login screen

from backend import storage
import customtkinter as ctk
from backend import auth

def login_screen(aa_app, aa_title, menu):
    user_data = storage.load_user_prof()

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
            placeholder_text_color='white',
            font=('Terminal', 15),
            show="*"
        )

    username_entry = ctk.CTkEntry(
        authentication_frame
    )
    username_entry.configure(
        placeholder_text='Username',
        placeholder_text_color='white',
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
            aa_subtitle,
            aa_app,
            menu,
            aa_title
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
            aa_subtitle,
            aa_app,
            menu,
            aa_title
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
def new_user(username_entry, password_entry, invalid_label, authentication_frame, aa_subtitle, aa_app, menu, aa_title):
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
    
    user_data = storage.load_user_prof()

    authentication_frame.destroy()
    aa_title.pack_forget()
    aa_subtitle.pack_forget()
    menu(aa_app, aa_title)
                
#function that will authenticate old user
def log_in(password_entry, invalid_label, authentication_frame, aa_subtitle, aa_app, menu, aa_title):
    #load in saved password
    user_data = storage.load_user_prof()
    
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
    menu(aa_app, aa_title)
