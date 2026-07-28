import customtkinter as ctk
from tkinter import TclError
from gui_style.typography import create_fonts
from gui_logic.log_in import login_screen
from gui_logic.menu import menu_screen
from gui_logic.navigation import set_aa_title

def maximize_window(window):
    """Start maximized while still allowing the window to be restored."""
    window.update_idletasks()
    try:
        window.attributes("-zoomed", True)
    except TclError:
        try:
            window.state("zoomed")
        except TclError:
            pass

aa_app = ctk.CTk()
fonts = create_fonts(aa_app)

#set title and window size
aa_app.title('Assignment Assessor')
aa_app.geometry('1100x800')
aa_app.minsize(1024, 700)
aa_app._set_appearance_mode("system")
aa_app.after(100, lambda: maximize_window(aa_app))

aa_app.grid_rowconfigure(0, weight=0)
aa_app.grid_columnconfigure(0, weight=1)
aa_app.grid_rowconfigure(1, weight=1)

#set title text
aa_title = ctk.CTkLabel(
    aa_app, 
    pady=25,
    text='Assignment Assessor',
    font=fonts["brand"],
    fg_color='transparent',
    corner_radius=10
)
aa_title.grid(row=0, column=0, padx=10, pady=10)

set_aa_title(aa_title)

content_frame = ctk.CTkFrame(
    aa_app,
    fg_color='transparent'
)
content_frame.grid(row=1, column=0, sticky='nsew')

content_frame.grid_rowconfigure(0, weight=1)
content_frame.grid_columnconfigure(0, weight=1)

login_screen(content_frame, aa_title, menu_screen, fonts)
aa_app.mainloop()
