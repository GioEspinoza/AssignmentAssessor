# AA_gui
import customtkinter as ctk
import 

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

aa = ctk.CTk()
aa.title("Assignment Assessor")
aa.geometry("400x300")

title = ctk.CTkLabel(
    aa, text="Assignment Assessor", font=ctk.CTkFont(size=22, weight="normal")
)
title.pack(pady=20)



aa.mainloop()