import customtkinter as ctk
from backend.session import get_current_user_id
from gui_style import colors, spacing
from database.course_queries import get_courses, archive_course, restore_course, delete_course, update_course

def open_edit_course_popup(parent, fonts, on_course_updated):
    popup = ctk.CTkToplevel(parent)

    popup.title("Edit Course")
    popup.geometry("820x500")
    popup.minsize(740, 380)
    popup.resizable(True, True)

    popup.transient(parent.winfo_toplevel())  # Keep the popup on top of the parent window

    content_frame = ctk.CTkFrame(
        popup,
        fg_color=colors.TRANSPARENT
    )
    content_frame.pack(
        expand=True,
        fill="both",
        padx=spacing.SPACE_8,
        pady=spacing.SPACE_6
    )
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_rowconfigure(1, weight=1)

    title = ctk.CTkLabel(
        content_frame,
        text="Edit Course",
        font=fonts["section_title"],
        text_color=colors.TEXT_PRIMARY
    )
    title.grid(
        row=0,
        column=0,
        sticky="w",
        pady=(0, spacing.SPACE_5)
    )

    course_list_frame = ctk.CTkScrollableFrame(
        content_frame,
        fg_color=colors.SURFACE,
        border_color=colors.BORDER,
        border_width=spacing.CARD_BORDER_WIDTH,
        corner_radius=spacing.RADIUS_LARGE
    )
    course_list_frame.grid(
        row=1,
        column=0,
        sticky="nsew"
    )
    course_list_frame.grid_columnconfigure(0, weight=1)

    action_icon_font = ctk.CTkFont(
        family=fonts["body_bold"].cget("family"),
        size=fonts["body_bold"].cget("size") + 6,
        weight="bold"
    )

    def finish_update():
        popup.destroy()
        on_course_updated()

    def set_course_active(course_to_update, active):
        if active:
            restore_course(get_current_user_id(), course_to_update)
        else:
            archive_course(get_current_user_id(), course_to_update)
        finish_update()

    for row, course in enumerate(get_courses(get_current_user_id())):
        current_course_id = course["course_id"]
        course_name = course["course_name"]
        course_code = course["course_code"]
        is_active = course["is_active"]

        status_text = "Active" if is_active else "Inactive"
        status_color = colors.SUCCESS if is_active else colors.DANGER
        course_color = status_color
        course_card_color = (
            ("#ECFDF5", "#163229")
            if is_active
            else ("#FEF2F2", "#3A2025")
        )

        course_frame = ctk.CTkFrame(
            course_list_frame,
            fg_color=course_card_color,
            border_color=course_color,
            border_width=spacing.CARD_BORDER_WIDTH,
            corner_radius=spacing.RADIUS_LARGE
        )
        course_frame.grid(
            row=row,
            column=0,
            sticky="ew",
            padx=spacing.SPACE_3,
            pady=(spacing.SPACE_3 if row == 0 else 0, spacing.SPACE_3)
        )
        course_frame.grid_columnconfigure(0, weight=1)
        course_frame.grid_columnconfigure(1, weight=0)
        course_frame.grid_columnconfigure(2, weight=0)

        course_label = ctk.CTkLabel(
            course_frame,
            text=course_name,
            font=fonts["body_bold"],
            text_color=course_color,
            anchor="w",
            justify="left",
            wraplength=390
        )
        course_label.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(spacing.SPACE_5, spacing.SPACE_4),
            pady=(spacing.SPACE_4, spacing.SPACE_1)
        )

        course_code_label = ctk.CTkLabel(
            course_frame,
            text=course_code or "No course code",
            font=fonts["body"],
            text_color=colors.TEXT_SECONDARY,
            anchor="w"
        )
        course_code_label.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(spacing.SPACE_5, spacing.SPACE_4),
            pady=(0, spacing.SPACE_4)
        )

        is_active_label = ctk.CTkLabel(
            course_frame,
            text=status_text,
            font=fonts["body"],
            text_color=status_color,
            fg_color=colors.TRANSPARENT,
            border_color=status_color,
            border_width=1,
            corner_radius=spacing.RADIUS_SMALL,
            width=88,
            height=36
        )
        is_active_label.grid(
            row=0,
            column=1,
            rowspan=2,
            sticky="e",
            padx=(spacing.SPACE_3, spacing.SPACE_4)
        )

        button_frame = ctk.CTkFrame(
            course_frame,
            fg_color=colors.TRANSPARENT
        )
        button_frame.grid(
            row=0,
            column=2,
            rowspan=2,
            sticky="e",
            padx=(0, spacing.SPACE_5)
        )

        archive_course_button = ctk.CTkButton(
            button_frame,
            text="↓" if is_active else "↻",
            font=action_icon_font,
            command=lambda selected_course_id=current_course_id,
                           active=is_active: set_course_active(
                               selected_course_id,
                               not active
            ),
            fg_color=colors.ACCENT,
            hover_color=colors.ACCENT_HOVER,
            corner_radius=spacing.RADIUS_MEDIUM,
            width=46,
            height=46,
            cursor="hand2"
        )
        archive_course_button.grid(
            row=0,
            column=0,
            padx=(0, spacing.SPACE_2)
        )

        edit_course_button = ctk.CTkButton(
            button_frame,
            text="✎",
            font=action_icon_font,
            command=lambda selected_course_id=current_course_id,
                           selected_name=course_name,
                           selected_code=course_code,
                           active=is_active: edit_course_popup(
                               popup,
                               fonts,
                               selected_course_id,
                               selected_name,
                               selected_code,
                               active,
                               finish_update
                           ),
            fg_color=colors.ACCENT,
            hover_color=colors.ACCENT_HOVER,
            corner_radius=spacing.RADIUS_MEDIUM,
            width=46,
            height=46,
            cursor="hand2"
        )
        edit_course_button.grid(
            row=0,
            column=1,
            padx=(0, spacing.SPACE_2)
        )

        delete_course_button = ctk.CTkButton(
            button_frame,
            text="×",
            font=action_icon_font,
            command=lambda selected_course_id=current_course_id,
                           selected_name=course_name: confirm_delete_popup(
                               popup,
                               fonts,
                               selected_course_id,
                               selected_name,
                               finish_update
                           ),
            fg_color=colors.DANGER,
            hover_color=("#B91C1C", "#DC2626"),
            corner_radius=spacing.RADIUS_MEDIUM,
            width=46,
            height=46,
            cursor="hand2"
        )
        delete_course_button.grid(
            row=0,
            column=2
        )


def confirm_delete_popup(
    parent,
    fonts,
    course_id,
    course_name,
    on_course_deleted
):
    popup = ctk.CTkToplevel(parent)

    popup.title("Confirm Delete")
    popup.geometry("400x200")

    popup.resizable(False, False)

    popup.transient(parent.winfo_toplevel())  # Keep the popup on top of the parent window

    # Create a frame for the content
    content_frame = ctk.CTkFrame(
        popup,
        fg_color='transparent'
    )
    content_frame.pack(expand=True, fill='both', padx=20, pady=20)

    # Confirmation Message
    message = ctk.CTkLabel(
        content_frame,
        text=f"Are you sure you want to delete the course '{course_name}'?",
        font=fonts["body_bold"],
        wraplength=350
    )
    message.pack(anchor='center', pady=(0, 20))

    # Button Frame
    button_frame = ctk.CTkFrame(
        content_frame,
        fg_color='transparent'
    )
    button_frame.pack(anchor='center')

    def confirm_delete():
        delete_course(get_current_user_id(), course_id)
        popup.destroy()
        on_course_deleted()

    # Confirm Button
    confirm_button = ctk.CTkButton(
        button_frame,
        text="Delete",
        font=fonts["body_bold"],
        command=confirm_delete,
        fg_color=colors.DANGER,
        hover_color=colors.DANGER,
        corner_radius=spacing.RADIUS_MEDIUM,
        width=100
    )
    confirm_button.pack(side='left', padx=10)

    # Cancel Button
    cancel_button = ctk.CTkButton(
        button_frame,
        text="Cancel",
        font=fonts["body_bold"],
        command=popup.destroy,
        fg_color=colors.ACCENT,
        hover_color=colors.ACCENT_HOVER,
        corner_radius=spacing.RADIUS_MEDIUM,
        width=100
    )
    cancel_button.pack(side='left', padx=10)

def edit_course_popup(
    parent,
    fonts,
    course_id,
    course_name,
    course_code,
    is_active,
    on_course_updated
):
    popup = ctk.CTkToplevel(parent)

    popup.title("Edit Course")
    popup.geometry("400x300")

    popup.resizable(False, False)

    popup.transient(parent.winfo_toplevel())  # Keep the popup on top of the parent window

    # Create a frame for the content
    content_frame = ctk.CTkFrame(
        popup,
        fg_color='transparent'
    )
    content_frame.pack(expand=True, fill='both', padx=20, pady=20)

    course_name_entry_label = ctk.CTkEntry(
        content_frame,
        width=300
    )
    course_name_entry_label.insert(0, course_name)
    course_name_entry_label.pack(anchor='w', pady=(0, 10))

    course_code_entry_label = ctk.CTkEntry(
        content_frame,
        width=300
    )
    course_code_entry_label.insert(0, course_code or "")
    course_code_entry_label.pack(anchor='w', pady=(0, 10))

    validation_label = ctk.CTkLabel(
        content_frame,
        text="",
        font=fonts["body"],
        text_color=colors.DANGER
    )
    validation_label.pack(anchor='w', pady=(0, 10))

    def save_changes():
        new_course_name = course_name_entry_label.get().strip()
        new_course_code = course_code_entry_label.get().strip()

        if not new_course_name:
            validation_label.configure(text="Course name cannot be empty.")
            return
        if len(new_course_name) > 100:
            validation_label.configure(
                text="Course name cannot exceed 100 characters."
            )
            return
        if len(new_course_code) > 30:
            validation_label.configure(
                text="Course code cannot exceed 30 characters."
            )
            return

        update_course(
            get_current_user_id(),
            course_id,
            new_course_name,
            new_course_code or None
        )
        popup.destroy()
        on_course_updated()

    submit_changes_button = ctk.CTkButton(
        content_frame,
        text="Submit Changes",
        font=fonts["body_bold"],
        command=save_changes
    )
    submit_changes_button.pack(anchor='center', pady=(0, 10))

    cancel_button = ctk.CTkButton(
        content_frame,
        text="Cancel",
        font=fonts["body_bold"],
        command=popup.destroy
    )
    cancel_button.pack(anchor='center', pady=(0, 10))
