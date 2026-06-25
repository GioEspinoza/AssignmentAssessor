#encapsulate login screen
from backend import session
from database import user_queries
import customtkinter as ctk
from backend import auth

def login_screen(aa_app, aa_title, menu):

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
            username_entry.get().strip(),
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

    aa_subtitle.configure(
    text="Welcome to AssignmentAssessor",
    font=("Terminal", 25)
    )

    aa_subtitle.pack(pady=10)

    username_entry.pack(pady=20)
    password_entry.pack(pady=10)
    log_in_button.pack(pady=10)
    register_button.pack(pady=10)
    authentication_frame.pack(pady=20, expand=True)
    authentication_frame.pack_propagate(False)
    
#function that will register new user
def new_user(username_entry, password_entry, invalid_label, authentication_frame, aa_subtitle, aa_app, menu, aa_title):
    #check if user and password are valid
    valid, message = auth.validate_username(username_entry)
    passvalid, passmessage = auth.validate_password(password_entry)
    
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
        
    password_hash = auth.hash_password(password_entry)


    existing_user = user_queries.get_user_by_username(username_entry)

    if existing_user is not None:
        invalid_label.configure(text="Username already exists")
        invalid_label.pack(pady=10)
        aa_app.after(2500, invalid_label.pack_forget)
        return
    
    created_user = user_queries.create_user(
        username_entry,
        None,
        password_hash
    )
    
    session.current_user = created_user

    authentication_frame.destroy()
    aa_title.pack_forget()
    aa_subtitle.pack_forget()
    menu(aa_app, aa_title)
                
#function that will authenticate old user
def log_in(username_entry, password_entry, invalid_label, authentication_frame, aa_subtitle, aa_app, menu, aa_title):
    #load in saved password
    user_data = user_queries.get_user_by_username(username_entry)
    
    if user_data is None:
        invalid_label.configure(text="User not found")
        invalid_label.pack(pady=10)
        aa_app.after(2500, invalid_label.pack_forget)
        return
    print(type(user_data["password_hash"]))
    print(repr(user_data["password_hash"]))
    if not auth.check_password(user_data["password_hash"], password_entry):
        #if not refresh label for invalid inputs
        invalid_label.configure(
            text="Incorrect password"
         )
        invalid_label.pack(
            pady=10
        )
        aa_app.after(2500, invalid_label.pack_forget)
        return
    
    session.current_user = user_data
    authentication_frame.destroy()
    aa_title.configure(
        font=("Terminal", 40),
        pady=5
    )
    aa_subtitle.pack_forget()
    menu(aa_app, aa_title)