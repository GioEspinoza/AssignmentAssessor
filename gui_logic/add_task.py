import customtkinter as ctk
from backend import course_service
from backend.session import get_current_user_id
from gui_style import colors, spacing
from gui_style.responsive import clone_fonts, ResponsiveText


def add_task(parent, fonts):
    base_fonts = fonts
    fonts = clone_fonts(fonts)

    for widget in parent.winfo_children():
        widget.destroy()

    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    add_task_frame = ctk.CTkFrame(
        parent,
        fg_color=colors.TRANSPARENT,
    )
    add_task_frame.grid(row=0, column=0, sticky="nsew")
    add_task_frame.grid_rowconfigure(0, weight=0)
    add_task_frame.grid_rowconfigure(1, weight=1)
    add_task_frame.grid_columnconfigure(0, weight=1)

    setattr(
        add_task_frame,
        "responsive_text",
        ResponsiveText(
            add_task_frame,
            fonts,
            base_width=900,
            min_scale=0.8,
            max_scale=1.25,
        ),
    )

    header_frame = ctk.CTkFrame(
        add_task_frame,
        fg_color=colors.TRANSPARENT,
    )
    header_frame.grid_columnconfigure(0, weight=1)
    header_frame.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=spacing.PAGE_X,
        pady=(spacing.PAGE_Y, spacing.SECTION_GAP),
    )

    title_label = ctk.CTkLabel(
        header_frame,
        text="Add Assignment",
        font=fonts["page_title"],
        text_color=colors.TEXT_PRIMARY,
    )
    subtitle_label = ctk.CTkLabel(
        header_frame,
        text="Fill out the form below to add a new assignment.",
        font=fonts["body"],
        text_color=colors.TEXT_SECONDARY,
    )

    title_label.grid(
        row=0,
        column=0,
        sticky="w"
        )

    subtitle_label.grid(
        row=1,
        column=0,
        sticky="w",
        pady=(spacing.SPACE_1, 0),
    )

    cancel_button = ctk.CTkButton(
        header_frame,
        text="Cancel",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
        fg_color=colors.SURFACE,
        hover_color=colors.SURFACE_HOVER,
        corner_radius=spacing.RADIUS_MEDIUM,
        command=lambda: back_to_assignments(parent, base_fonts),
    )
    cancel_button.grid(
        row=0,
        column=1,
        sticky="e",
        padx=(0, spacing.CARD_PADDING),
    )

    form_card = ctk.CTkFrame(
        add_task_frame,
        fg_color=colors.SURFACE,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
        corner_radius=spacing.RADIUS_LARGE,
    )
    form_card.grid(
        row=1,
        column=0,
        sticky="new",
        padx=spacing.PAGE_X,
        pady=(0, spacing.PAGE_Y),
    )
    form_card.grid_columnconfigure(0, weight=1)

    status_label = ctk.CTkLabel(
        form_card,
        text="Assignment status",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    status_label.grid(
        row=0,
        column=0,
        sticky="w",
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_2),
    )

    status_value = ctk.StringVar(value="Not Started")
    status_control = ctk.CTkSegmentedButton(
        form_card,
        values=["Not Started", "In Progress", "Completed"],
        variable=status_value,
        font=fonts["body"],
        text_color=colors.TEXT_PRIMARY,
        selected_color=colors.ACCENT,
        selected_hover_color=colors.ACCENT_HOVER,
        unselected_color=colors.SURFACE_HOVER,
        unselected_hover_color=colors.BORDER,
        corner_radius=spacing.RADIUS_MEDIUM,
        height=38,
    )
    status_control.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=spacing.CARD_PADDING,
    )

    status_helper = ctk.CTkLabel(
        form_card,
        text="Choose the assignment's current progress status.",
        font=fonts["small"],
        text_color=colors.TEXT_SECONDARY,
    )
    status_helper.grid(
        row=2,
        column=0,
        sticky="w",
        padx=spacing.CARD_PADDING,
        pady=(spacing.SPACE_2, spacing.CARD_PADDING),
    )
    
    course_label = ctk.CTkLabel(
        form_card,
        text="Course name",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    course_label.grid(
        row=3,
        column=0,
        sticky="w",
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_2),
    )

    courses = get_courses_for_user(get_current_user_id())
    
    if not courses:
        no_courses_label = ctk.CTkLabel(
            form_card,
            text="No active courses found. Please add a course first.",
            font=fonts["small"],
            text_color=colors.TEXT_SECONDARY,
        )
        no_courses_label.grid(
            row=5,
            column=0,
            sticky="w",
            padx=spacing.CARD_PADDING,
            pady=(spacing.SPACE_2, spacing.CARD_PADDING),
        )
        add_course_button = ctk.CTkButton(
            form_card,
            text="Add Course",
            font=fonts["body_bold"],
            text_color=colors.TEXT_PRIMARY,
            fg_color=colors.ACCENT,
            hover_color=colors.SURFACE_HOVER,
            border_color=colors.BORDER,
            corner_radius=spacing.RADIUS_MEDIUM,
            #command=lambda: add_course_screen(parent, base_fonts),
        )

        add_course_button.grid(
            row=5,
            column=1,
            sticky="e",
            padx=(0, spacing.CARD_PADDING),
        )
    else:
        course_helper = ctk.CTkLabel(
            form_card,
            text="Select the course to which this assignment belongs.",
            font=fonts["small"],
            text_color=colors.TEXT_SECONDARY,
        )
        course_helper.grid(
            row=4,
            column=0,
            sticky="w",
            padx=spacing.CARD_PADDING,
            pady=(spacing.SPACE_2, spacing.CARD_PADDING),
        )

        course_dropdown = ctk.CTkOptionMenu(
            form_card,
            values=courses,
            font=fonts["body"],
            text_color=colors.TEXT_PRIMARY,
            button_color=colors.SURFACE,
            button_hover_color=colors.SURFACE_HOVER,
            dropdown_fg_color=colors.SURFACE,
            dropdown_hover_color=colors.SURFACE_HOVER,
            corner_radius=spacing.RADIUS_MEDIUM,
        )
        course_dropdown.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=spacing.CARD_PADDING,
        )


    
def back_to_assignments(parent, fonts):
    from gui_logic.assignments import assignments_screen
    assignments_screen(parent, fonts)

def get_courses_for_user(user_id):
    courses = course_service.get_active_courses(user_id)
    return [course["course_name"] for course in courses]
