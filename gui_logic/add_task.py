import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry
from backend import course_service
from backend.session import get_current_user_id
from gui_style import colors, spacing
from gui_style.responsive import clone_fonts, ResponsiveText
from gui_widgets.widgets import enable_linux_mousewheel

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

    form_card = ctk.CTkScrollableFrame(
        add_task_frame,
        fg_color=colors.SURFACE,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
        corner_radius=spacing.RADIUS_LARGE,
        scrollbar_button_color=colors.BORDER,
        scrollbar_button_hover_color=colors.TEXT_SECONDARY,
    )
    form_card.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=spacing.PAGE_X,
        pady=(0, spacing.PAGE_Y),
    )
    form_card.grid_columnconfigure(
        (0, 1),
        weight=1,
        uniform="assignment_form_columns",
    )

    form_card_label = ctk.CTkLabel(
        form_card,
        text="Assignment Details",
        font=fonts["card_title"],
        text_color=colors.TEXT_PRIMARY,
    )
    form_card_label.grid(
        row=0,
        column=0,
        sticky="w",
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_2),
    )

    status_label = ctk.CTkLabel(
        form_card,
        text="Assignment status",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    status_label.grid(
        row=1,
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
        row=2,
        column=0,
        columnspan=2,
        sticky="ew",
        padx=spacing.CARD_PADDING,
    )

    task_name_label = ctk.CTkLabel(
            form_card,
            text="Assignment name",
            font=fonts["body_bold"],
            text_color=colors.TEXT_PRIMARY,
        )
    task_name_label.grid(
            row=3,
            column=0,
            sticky="w",
            padx=spacing.CARD_PADDING,
            pady=(spacing.CARD_PADDING, spacing.SPACE_2),
        )

    task_name_entry = ctk.CTkEntry(
            form_card,
            font=fonts["body"],
            text_color=colors.TEXT_PRIMARY,
            fg_color=colors.SURFACE,
            border_color=colors.BORDER,
            corner_radius=spacing.RADIUS_MEDIUM,
        )
    task_name_entry.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=spacing.CARD_PADDING,
            pady=(spacing.CARD_PADDING, spacing.SPACE_2),
        )
    course_section = ctk.CTkFrame(
        form_card,
        fg_color=colors.TRANSPARENT,
    )
    course_section.grid(
        row=5,
        column=0,
        sticky="nsew",
        padx=(spacing.CARD_PADDING, spacing.SPACE_2),
        pady=spacing.CARD_PADDING,
    )
    course_section.grid_columnconfigure(
        (0, 1),
        weight=1,
        uniform="course_heading",
    )

    course_label = ctk.CTkLabel(
        course_section,
        text="Course name",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    course_label.grid(
        row=0,
        column=0,
        sticky="w",
    )

    courses = get_courses_for_user(get_current_user_id())

    if not courses:
        no_courses_label = ctk.CTkLabel(
            course_section,
            text="No active courses found. Please add a course first.",
            font=fonts["small"],
            text_color=colors.TEXT_SECONDARY,
        )
        no_courses_label.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(spacing.SPACE_3, 0),
        )

        add_course_button = ctk.CTkButton(
            course_section,
            text="Add Course",
            font=fonts["body_bold"],
            text_color=colors.TEXT_ON_ACCENT,
            fg_color=colors.ACCENT,
            hover_color=colors.ACCENT_HOVER,
            border_color=colors.BORDER,
            corner_radius=spacing.RADIUS_MEDIUM,
            height=38,
            #command=lambda: add_course_screen(parent, base_fonts),
        )
        add_course_button.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(spacing.SPACE_3, 0),
        )


    else:
        course_dropdown = ctk.CTkOptionMenu(
            course_section,
            values=courses,
            font=fonts["body"],
            text_color=colors.TEXT_PRIMARY,
            fg_color=colors.SURFACE,
            button_color=colors.SURFACE,
            button_hover_color=colors.SURFACE_HOVER,
            dropdown_fg_color=colors.SURFACE,
            dropdown_hover_color=colors.SURFACE_HOVER,
            corner_radius=spacing.RADIUS_MEDIUM,
            height=38,
        )
        course_dropdown.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(spacing.SPACE_3, 0),
        )


    date_time_section = ctk.CTkFrame(
        form_card,
        fg_color=colors.TRANSPARENT,
    )
    date_time_section.grid(
        row=5,
        column=1,
        sticky="nsew",
        padx=(spacing.SPACE_2, spacing.CARD_PADDING),
        pady=spacing.CARD_PADDING,
    )
    date_time_section.grid_columnconfigure(0, weight=0)
    date_time_section.grid_columnconfigure(1, weight=1)

    date_label = ctk.CTkLabel(
        date_time_section,
        text="Date and time",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    date_label.grid(
        row=0,
        column=0,
        sticky="w",
    )

    appearance_index = (
        1 if ctk.get_appearance_mode().casefold() == "dark" else 0
    )

    def resolve_color(color):
        if isinstance(color, tuple):
            return color[appearance_index]
        return color

    date_entry_style = ttk.Style(date_time_section)
    date_entry_style.configure(
        "Assignment.DateEntry",
        fieldbackground=resolve_color(colors.SURFACE),
        background=resolve_color(colors.ACCENT),
        foreground=resolve_color(colors.TEXT_PRIMARY),
        arrowcolor=colors.TEXT_ON_ACCENT,
        bordercolor=resolve_color(colors.BORDER),
        lightcolor=resolve_color(colors.BORDER),
        darkcolor=resolve_color(colors.BORDER),
        insertcolor=resolve_color(colors.TEXT_PRIMARY),
        padding=(spacing.SPACE_3, spacing.SPACE_2),
        font=(
            fonts["body"].cget("family"),
            fonts["body"].cget("size"),
        ),
    )
    date_entry_style.map(
        "Assignment.DateEntry",
        fieldbackground=[
            ("readonly", resolve_color(colors.SURFACE)),
            ("focus", resolve_color(colors.SURFACE)),
        ],
        bordercolor=[
            ("focus", resolve_color(colors.ACCENT)),
        ],
    )

    date_date_entry = DateEntry(
        date_time_section,
        date_pattern="yyyy-mm-dd",
        style="Assignment.DateEntry",
        background=resolve_color(colors.ACCENT),
        foreground=colors.TEXT_ON_ACCENT,
        headersbackground=resolve_color(colors.SURFACE_HOVER),
        headersforeground=resolve_color(colors.TEXT_PRIMARY),
        normalbackground=resolve_color(colors.SURFACE),
        normalforeground=resolve_color(colors.TEXT_PRIMARY),
        weekendbackground=resolve_color(colors.SURFACE),
        weekendforeground=resolve_color(colors.DANGER),
        othermonthbackground=resolve_color(colors.SURFACE_HOVER),
        othermonthforeground=resolve_color(colors.TEXT_SECONDARY),
        selectbackground=resolve_color(colors.ACCENT),
        selectforeground=colors.TEXT_ON_ACCENT,
        bordercolor=resolve_color(colors.BORDER),
    )

    date_date_entry.grid(
        row=1,
        column=0,
        columnspan=2,
        sticky="ew",
        pady=(spacing.SPACE_3, spacing.SPACE_4),
    )

    time_frame = ctk.CTkFrame(
        date_time_section,
        fg_color=colors.TRANSPARENT,
    )
    time_frame.grid(
        row=2,
        column=0,
        columnspan=2,
        sticky="ew",
    )
    time_frame.grid_columnconfigure((0, 1), weight=1, uniform="time_fields")
    time_frame.grid_columnconfigure(2, weight=0)

    hour_label = ctk.CTkLabel(
        time_frame,
        text="Hour",
        font=fonts["small_bold"],
        text_color=colors.TEXT_SECONDARY,
    )
    hour_label.grid(row=0, column=0, sticky="w")

    hour_entry = ctk.CTkComboBox(
        time_frame,
        values=[f"{i:02d}" for i in range(13)],
        font=fonts["body"],
        dropdown_font=fonts["body"],
        text_color=colors.TEXT_PRIMARY,
        fg_color=colors.SURFACE,
        border_color=colors.BORDER,
        button_color=colors.ACCENT,
        button_hover_color=colors.ACCENT_HOVER,
        dropdown_fg_color=colors.SURFACE,
        dropdown_hover_color=colors.SURFACE_HOVER,
        dropdown_text_color=colors.TEXT_PRIMARY,
        corner_radius=spacing.RADIUS_MEDIUM,
        height=38,
    )
    hour_entry.set("12")
    hour_entry.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=(0, spacing.SPACE_2),
        pady=(spacing.SPACE_1, 0),
    )

    minute_label = ctk.CTkLabel(
        time_frame,
        text="Minute",
        font=fonts["small_bold"],
        text_color=colors.TEXT_SECONDARY,
    )
    minute_label.grid(row=0, column=1, sticky="w")

    minute_entry = ctk.CTkComboBox(
        time_frame,
        values=["00", "15", "30", "45", "59"],
        font=fonts["body"],
        dropdown_font=fonts["body"],
        text_color=colors.TEXT_PRIMARY,
        fg_color=colors.SURFACE,
        border_color=colors.BORDER,
        button_color=colors.ACCENT,
        button_hover_color=colors.ACCENT_HOVER,
        dropdown_fg_color=colors.SURFACE,
        dropdown_hover_color=colors.SURFACE_HOVER,
        dropdown_text_color=colors.TEXT_PRIMARY,
        corner_radius=spacing.RADIUS_MEDIUM,
        height=38,
    )
    minute_entry.set("00")
    minute_entry.grid(
        row=1,
        column=1,
        sticky="ew",
        padx=(spacing.SPACE_2, 0),
        pady=(spacing.SPACE_1, 0),
    )

    am_pm_label = ctk.CTkLabel(
        time_frame,
        text="Period",
        font=fonts["small_bold"],
        text_color=colors.TEXT_SECONDARY,
    )
    am_pm_label.grid(
        row=0,
        column=2,
        sticky="w",
        padx=(spacing.GRID_GAP, 0),
    )

    am_pm_entry = ctk.CTkSegmentedButton(
        time_frame,
        values=["AM", "PM"],
        font=fonts["body"],
        text_color=colors.TEXT_PRIMARY,
        selected_color=colors.ACCENT,
        selected_hover_color=colors.ACCENT_HOVER,
        unselected_color=colors.SURFACE_HOVER,
        unselected_hover_color=colors.BORDER,
        corner_radius=spacing.RADIUS_MEDIUM,
        height=38,
    )
    am_pm_entry.set("AM")
    am_pm_entry.grid(
        row=1,
        column=2,
        sticky="e",
        padx=(spacing.GRID_GAP, 0),
        pady=(spacing.SPACE_1, 0),
    )

    short_desc_section = ctk.CTkFrame(
        form_card,
        fg_color=colors.TRANSPARENT,
    )
    short_desc_section.grid(
        row=6,
        column=0,
        columnspan=2,
        sticky="ew",
        padx=spacing.CARD_PADDING,
        pady=(0, spacing.CARD_PADDING),
    )
    short_desc_section.grid_columnconfigure(0, weight=1)

    short_desc = ctk.CTkLabel(
        short_desc_section,
        text="Short description",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    short_desc.grid(
        row=0,
        column=0,
        sticky="w",
    )

    short_desc_helper = ctk.CTkLabel(
        short_desc_section,
        text="Optional",
        font=fonts["small"],
        text_color=colors.TEXT_SECONDARY,
    )
    short_desc_helper.grid(
        row=0,
        column=1,
        sticky="e",
    )

    short_desc_entry = ctk.CTkTextbox(
        short_desc_section,
        font=fonts["body"],
        text_color=resolve_color(colors.TEXT_PRIMARY),
        fg_color=colors.SURFACE_HOVER,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
        corner_radius=spacing.RADIUS_MEDIUM,
        height=120,
    )
    short_desc_entry.grid(
        row=1,
        column=0,
        columnspan=2,
        sticky="ew",
        pady=(spacing.SPACE_2, 0),
    )

    tags_section = ctk.CTkFrame(
        form_card,
        fg_color=colors.TRANSPARENT,
    )
    tags_section.grid(
        row=7,
        column=0,
        columnspan=2,
        sticky="ew",
        padx=spacing.CARD_PADDING,
        pady=(0, spacing.CARD_PADDING),
    )
    tags_section.grid_columnconfigure(0, weight=1)

    tags_label = ctk.CTkLabel(
        tags_section,
        text="Tags",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    tags_label.grid(
        row=0,
        column=0,
        sticky="w",
    )

    tags_helper = ctk.CTkLabel(
        tags_section,
        text="Optional",
        font=fonts["small"],
        text_color=colors.TEXT_SECONDARY,
    )
    tags_helper.grid(
        row=0,
        column=1,
        sticky="e",
    )

    tags_button = ctk.CTkButton(
        tags_section,
        text="+ Tag",
        font=fonts["body_bold"],
        text_color=colors.TEXT_ON_ACCENT,
        fg_color=colors.ACCENT,
        hover_color=colors.ACCENT_HOVER,
        border_color=colors.BORDER,
        corner_radius=spacing.RADIUS_MEDIUM,
        height=38,
        #command=lambda: add_tags_screen(parent, base_fonts),
    )
    tags_button.grid(
        row=1,
        column=0,
        columnspan=2,
        sticky="ew",
        pady=(spacing.SPACE_2, 0),
    )

    enable_linux_mousewheel(form_card)
    
def back_to_assignments(parent, fonts):
    from gui_logic.assignments import assignments_screen
    assignments_screen(parent, fonts)

def get_courses_for_user(user_id):
    courses = course_service.get_active_courses(user_id)
    return [course["course_name"] for course in courses]
