import webbrowser

import customtkinter as ctk

from backend import auth_service
from gui_style.responsive import clone_fonts, ResponsiveText


def open_forgot_password_user_link():
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


def login_screen(parent, aa_title, menu, fonts):
    base_fonts = fonts
    fonts = clone_fonts(fonts)
    if aa_title is not None:
        aa_title.configure(font=fonts["brand"])

    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    login_container = ctk.CTkFrame(parent, fg_color="transparent")
    login_container.grid(row=0, column=0, sticky="nsew")
    login_container.grid_rowconfigure(0, weight=1)
    login_container.grid_columnconfigure(0, weight=1)
    setattr(
        login_container,
        "responsive_text",
        ResponsiveText(
            login_container,
            fonts,
            base_width=1100,
            min_scale=0.85,
            max_scale=1.25,
        ),
    )

    authentication_frame = ctk.CTkTabview(
        login_container,
        width=700,
        height=570,
        corner_radius=19,
        segmented_button_font=fonts["button"],
        anchor="nw"
    )

    authentication_frame.add("Log in")
    login_tab = authentication_frame.tab("Log in")
    login_tab.grid_columnconfigure(0, weight=1)
    login_tab.configure(fg_color="transparent")

    authentication_frame.add("Register")
    register_tab = authentication_frame.tab("Register")
    register_tab.grid_columnconfigure(0, weight=1)
    register_tab.configure(fg_color="transparent")

    authentication_frame.set("Log in")
    # Keep both pages fixed and blend the tab control into the tab body.
    authentication_frame.grid_propagate(False)
    tab_color = authentication_frame.cget("fg_color")
    authentication_frame._segmented_button.configure(
        width=220,
        height=34,
        corner_radius=8,
        border_width=0,
        fg_color=tab_color,
        unselected_color=tab_color,
        unselected_hover_color=tab_color
    )

    # Log-in tab widgets
    login_subtitle = ctk.CTkLabel(
        login_tab,
        text="Welcome back",
        font=fonts["page_title"]
    )
    login_instruction = ctk.CTkLabel(
        login_tab,
        text="Sign in to manage your assignments",
        font=fonts["body"],
        text_color="gray70"
    )
    login_username_label = ctk.CTkLabel(
        login_tab,
        text="Username",
        font=fonts["body_bold"]
    )
    login_username_entry = ctk.CTkEntry(
        login_tab,
        placeholder_text="Enter your username or email",
        font=fonts["input"],
        height=42
    )
    login_password_label = ctk.CTkLabel(
        login_tab,
        text="Password",
        font=fonts["body_bold"]
    )
    login_password_entry = ctk.CTkEntry(
        login_tab,
        placeholder_text="Enter your password",
        font=fonts["input"],
        show="*",
        height=42
    )
    forgot_login_link = ctk.CTkLabel(
        login_tab,
        text="Forgot username or password?",
        font=fonts["small"],
        text_color=("#2563eb", "#60a5fa"),
        cursor="hand2"
    )
    forgot_login_link.bind(
        "<Button-1>",
        lambda event: open_forgot_password_user_link()
    )
    login_invalid_label = ctk.CTkLabel(
        login_tab,
        font=fonts["small_bold"],
        text_color="#ef4444",
        text=""
    )
    log_in_button = ctk.CTkButton(
        login_tab,
        height=42,
        corner_radius=10,
        text="Log in",
        font=fonts["button"],
        command=lambda: log_in(
            login_username_entry.get().strip(),
            login_password_entry.get(),
            login_invalid_label,
            login_container,
            parent,
            menu,
            aa_title,
            base_fonts
        )
    )

    login_subtitle.grid(row=0, column=0, padx=50, pady=(30, 2))
    login_instruction.grid(row=1, column=0, padx=50, pady=(0, 30))
    login_username_label.grid(row=2, column=0, padx=50, pady=(0, 8), sticky="w")
    login_username_entry.grid(row=3, column=0, padx=50, sticky="ew")
    login_password_label.grid(row=4, column=0, padx=50, pady=(22, 8), sticky="w")
    login_password_entry.grid(row=5, column=0, padx=50, sticky="ew")
    forgot_login_link.grid(row=6, column=0, padx=50, pady=(6, 0), sticky="w")
    login_invalid_label.grid(row=7, column=0, padx=50, pady=16, sticky="w")
    log_in_button.grid(row=8, column=0, padx=50, pady=(0, 30), sticky="ew")

    # Registration tab widgets
    register_subtitle = ctk.CTkLabel(
        register_tab,
        text="Create an account",
        font=fonts["page_title"]
    )
    register_instruction = ctk.CTkLabel(
        register_tab,
        text="Register to start managing your assignments",
        font=fonts["body"],
        text_color="gray70"
    )
    register_username_label = ctk.CTkLabel(
        register_tab,
        text="Username",
        font=fonts["body_bold"]
    )
    register_username_entry = ctk.CTkEntry(
        register_tab,
        placeholder_text="Choose a username",
        font=fonts["input"],
        height=42
    )
    register_email_label = ctk.CTkLabel(
        register_tab,
        text="Email",
        font=fonts["body_bold"]
    )
    register_email_entry = ctk.CTkEntry(
        register_tab,
        placeholder_text="Enter your email",
        font=fonts["input"],
        height=42
    )
    register_password_label = ctk.CTkLabel(
        register_tab,
        text="Password",
        font=fonts["body_bold"]
    )
    register_password_entry = ctk.CTkEntry(
        register_tab,
        placeholder_text="Create a password",
        font=fonts["input"],
        show="*",
        height=42
    )
    register_invalid_label = ctk.CTkLabel(
        register_tab,
        font=fonts["small_bold"],
        text_color="#ef4444",
        text=""
    )
    register_button = ctk.CTkButton(
        register_tab,
        corner_radius=10,
        height=42,
        text="Register",
        font=fonts["button"],
        command=lambda: new_user(
            register_username_entry.get().strip(),
            register_email_entry.get().strip(),
            register_password_entry.get(),
            register_invalid_label,
            login_container,
            parent,
            menu,
            aa_title,
            base_fonts
        )
    )

    register_subtitle.grid(row=0, column=0, padx=50, pady=(22, 2))
    register_instruction.grid(row=1, column=0, padx=50, pady=(0, 20))
    register_username_label.grid(row=2, column=0, padx=50, pady=(0, 6), sticky="w")
    register_username_entry.grid(row=3, column=0, padx=50, sticky="ew")
    register_email_label.grid(row=4, column=0, padx=50, pady=(14, 6), sticky="w")
    register_email_entry.grid(row=5, column=0, padx=50, sticky="ew")
    register_password_label.grid(row=6, column=0, padx=50, pady=(14, 6), sticky="w")
    register_password_entry.grid(row=7, column=0, padx=50, sticky="ew")
    register_invalid_label.grid(row=8, column=0, padx=50, pady=10)
    register_button.grid(row=9, column=0, padx=50, pady=(0, 22), sticky="ew")

    authentication_frame.grid(row=0, column=0, padx=50, pady=32)
    
    login_password_entry.bind("<Return>", lambda event: log_in_button.invoke())
    register_password_entry.bind("<Return>", lambda event: register_button.invoke())

def show_error(parent, invalid_label, message):
    invalid_label.configure(text=message)
    parent.after(
        2500,
        lambda: invalid_label.configure(text="")
    )


#function that will register new user
def new_user(username_entry, email_entry, password_entry, invalid_label, login_container, parent, menu, aa_title, fonts):
    user, error = auth_service.register_user(
        username_entry,
        email_entry,
        password_entry,
    )
    if error is not None:
        show_error(parent, invalid_label, error)
        return

    if aa_title is not None:
        aa_title.grid_remove()
    login_container.destroy()
    menu(parent, fonts, user["username"])

#function that will authenticate old user
def log_in(username_entry, password_entry, invalid_label, login_container, parent, menu, aa_title, fonts):
    user, error = auth_service.authenticate_user(
        username_entry,
        password_entry,
    )
    if error is not None:
        show_error(parent, invalid_label, error)
        return

    if aa_title is not None:
        aa_title.grid_remove()
    login_container.destroy()
    menu(parent, fonts, user["username"])
