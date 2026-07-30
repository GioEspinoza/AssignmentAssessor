import customtkinter as ctk
from backend.session import get_current_user_id
from gui_style import colors, spacing
from database.course_queries import add_course

def open_add_course_popup(parent, fonts, on_course_added):
    popup = ctk.CTkToplevel(parent)

    popup.title("Add Course")
    popup.geometry("420x300")

    popup.resizable(False, False)

    popup.transient(parent.winfo_toplevel())  # Keep the popup on top of the parent window

    # Create a frame for the content
    content_frame = ctk.CTkFrame(
        popup,
        fg_color='transparent'
    )
    content_frame.pack(expand=True, fill='both', padx=20, pady=20)

    # Add Course Title
    title = ctk.CTkLabel(
        content_frame,
        text="Add New Course",
        font=fonts["section_title"]
        )
    title.pack(anchor='center', pady=(0, 20))

    # Course Name Label and Entry
    course_name_label = ctk.CTkLabel(
        content_frame,
        text="Course Name:",
        font=fonts["body_bold"]
        )
    course_name_label.pack(anchor='w', pady=(0, 5))

    course_name_entry = ctk.CTkEntry(
        content_frame,
        placeholder_text="Enter course name",
        width=300
        )
    course_name_entry.pack(anchor='w', pady=(0, 10))

    # Course Code Label and Entry
    course_code_label = ctk.CTkLabel(
        content_frame,
        text="Course Code:",
        font=fonts["body_bold"]
        )
    course_code_label.pack(anchor='w', pady=(0, 5))

    course_code_entry = ctk.CTkEntry(
        content_frame,
        placeholder_text="Enter course code (optional)",
        width=300
        )
    course_code_entry.pack(anchor='w', pady=(0, 10))

    # Add Course Button
    add_course_button = ctk.CTkButton(
        content_frame,
        text="Add Course",
        font=fonts["body_bold"],
        command=lambda: submit_course(
            course_name_entry.get(),
            course_code_entry.get(),
            popup,
            on_course_added,
        ),
        fg_color=colors.ACCENT,
        hover_color=colors.ACCENT_HOVER,
        corner_radius=spacing.RADIUS_MEDIUM,
        height=30,
        width=100
    )
    add_course_button.pack(anchor='e', pady=(10, 0))

    popup.wait_visibility()
    popup.grab_set()  # Make the popup modal
    course_name_entry.focus_set()

def submit_course(course_name, course_code, popup, on_course_added):
    course_name = course_name.strip()
    course_code = course_code.strip()

    if len(course_name) > 100:
        # Show an error message if the course name is too long
        error_popup = ctk.CTkToplevel(popup)
        error_popup.title("Error")
        error_popup.geometry("300x150")
        error_popup.resizable(False, False)

        error_label = ctk.CTkLabel(
            error_popup,
            text="Course name cannot exceed 100 characters.",
            font=("Arial", 12),
            fg_color='transparent'
        )
        error_label.pack(expand=True, fill='both', padx=20, pady=20)

        ok_button = ctk.CTkButton(
            error_popup,
            text="OK",
            command=error_popup.destroy,
            fg_color=colors.ACCENT,
            hover_color=colors.ACCENT_HOVER,
            corner_radius=spacing.RADIUS_MEDIUM,
            height=30,
            width=80
        )
        ok_button.pack(anchor='center', pady=(0, 20))
        return
    elif not course_name:
        # Show an error message if the course name is empty
        error_popup = ctk.CTkToplevel(popup)
        error_popup.title("Error")
        error_popup.geometry("300x150")
        error_popup.resizable(False, False)

        error_label = ctk.CTkLabel(
            error_popup,
            text="Course name cannot be empty.",
            font=("Arial", 12),
            fg_color='transparent'
        )
        error_label.pack(expand=True, fill='both', padx=20, pady=20)

        ok_button = ctk.CTkButton(
            error_popup,
            text="OK",
            command=error_popup.destroy,
            fg_color=colors.ACCENT,
            hover_color=colors.ACCENT_HOVER,
            corner_radius=spacing.RADIUS_MEDIUM,
            height=30,
            width=80
        )
        ok_button.pack(anchor='center', pady=(0, 20))
        return
    if len(course_code) > 30:
        # Show an error message if the course code is too long
        error_popup = ctk.CTkToplevel(popup)
        error_popup.title("Error")
        error_popup.geometry("300x150")
        error_popup.resizable(False, False)

        error_label = ctk.CTkLabel(
            error_popup,
            text="Course code cannot exceed 30 characters.",
            font=("Arial", 12),
            fg_color='transparent'
        )
        error_label.pack(expand=True, fill='both', padx=20, pady=20)

        ok_button = ctk.CTkButton(
            error_popup,
            text="OK",
            command=error_popup.destroy,
            fg_color=colors.ACCENT,
            hover_color=colors.ACCENT_HOVER,
            corner_radius=spacing.RADIUS_MEDIUM,
            height=30,
            width=80
        )
        ok_button.pack(anchor='center', pady=(0, 20))
        return
    elif not course_code:
        course_code = None  # Set course_code to None if it's empty

    user_id = get_current_user_id()
    add_course(user_id, course_name, course_code)
    popup.destroy()
    on_course_added(course_name)
