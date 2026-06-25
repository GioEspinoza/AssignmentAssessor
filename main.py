import customtkinter as ctk
from gui_logic.log_in import login_screen
from gui_logic.menu import menu_screen
from gui_logic.navigation import set_aa_title

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

set_aa_title(aa_title)
aa_title.pack(pady=30)
login_screen(aa_app, aa_title, menu_screen)
aa_app.mainloop()
