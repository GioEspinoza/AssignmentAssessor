import customtkinter as ctk
from backend import session
import datetime
#will show menu after authencation

def get_time_of_day():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def menu_screen(parent, fonts, username=None):
    if not isinstance(username, str):
        if username is None:
            if session.current_user is None:
                 raise RuntimeError("No user is currently logged in.")
            username = session.current_user["username"]
        

    for widget in parent.winfo_children():
        widget.destroy()

    dashboard_frame = ctk.CTkFrame(
        parent,
        fg_color='transparent'
    )
    title_label = ctk.CTkLabel(
        dashboard_frame,
        text=f"{get_time_of_day()}, {username}!",
        font=fonts["display"],
        fg_color='transparent'
    )
    separator = ctk.CTkFrame(
        dashboard_frame,
        height=2,
        corner_radius=0,
        fg_color=("gray75", "gray30")
    )
    subtitle_label = ctk.CTkLabel(
        dashboard_frame,
        text="Dashboard",
        font=fonts["subtitle"],
        text_color='gray70',
        fg_color='transparent'
    )

    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    dashboard_frame.grid(row=0, column=0, sticky='nsew')
    dashboard_frame.grid_rowconfigure((0, 1, 2), weight=0)
    dashboard_frame.grid_rowconfigure(3, weight=1)
    dashboard_frame.grid_columnconfigure(0, weight=1)

    title_label.grid(row=0, column=0, padx=30, pady=(20, 12), sticky="nw")
    separator.grid(row=1, column=0, sticky="ew")
    subtitle_label.grid(row=2, column=0, padx=30, pady=(12, 20), sticky="nw")

    return dashboard_frame
