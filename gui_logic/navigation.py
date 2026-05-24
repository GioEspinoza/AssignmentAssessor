from backend import aa_logic

_aa_title = None


def set_aa_title(aa_title):
    global _aa_title
    if aa_title is not None:
        _aa_title = aa_title


def get_aa_title(aa_title=None):
    return aa_title if aa_title is not None else _aa_title


def update_checkbox_text(checkbox):
    checkbox.configure(
        font=('Terminal', 20),
        text=f"{checkbox.get()}"
    )


def check_not_empty_gui(course, task, hours):
    return (
        aa_logic.is_not_empty(course)
        and aa_logic.is_not_empty(task)
        and aa_logic.is_not_empty(hours)
    )


def back_to_menu(aa_app, frame, button_or_label, aa_title=None):
    from gui_logic.menu import menu_screen

    aa_title = get_aa_title(aa_title)
    frame.pack_forget()
    frame.destroy()
    button_or_label.destroy()
    aa_app.geometry('800x600')
    menu_screen(aa_app, aa_title)


def back_to_login(aa_app, aa_title, frame, quit_button):
    from gui_logic.log_in import login_screen
    from gui_logic.menu import menu_screen

    aa_title = get_aa_title(aa_title)
    frame.destroy()
    quit_button.destroy()
    aa_app.geometry('800x600')
    if aa_title is not None and not aa_title.winfo_manager():
        aa_title.pack(pady=30)
    login_screen(aa_app, aa_title, menu_screen)
