import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry
from backend import course_service, task_rules, task_service
from backend.session import get_current_user_id
from database import task_queries
from gui_style import colors, spacing
from gui_style.responsive import clone_fonts, ResponsiveText
from gui_widgets.widgets import enable_linux_mousewheel

def add_task(parent, fonts):
    base_fonts = fonts
    fonts = clone_fonts(fonts)
    parent.winfo_toplevel().minsize(1260, 700)

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
        sticky="nsew",
        padx=spacing.PAGE_X,
        pady=(0, spacing.PAGE_Y),
    )
    form_card.grid_rowconfigure(0, weight=1)
    form_card.grid_columnconfigure(0, weight=7)
    form_card.grid_columnconfigure(1, weight=3)

    assignment_details_frame = ctk.CTkScrollableFrame(
        form_card,
        fg_color=colors.SURFACE_HOVER,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
        corner_radius=spacing.RADIUS_LARGE,
        scrollbar_button_color=colors.BORDER,
        scrollbar_button_hover_color=colors.TEXT_SECONDARY,
    )
    assignment_details_frame.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(spacing.CARD_PADDING, spacing.SPACE_2),
        pady=spacing.CARD_PADDING,
    )
    assignment_details_frame.grid_columnconfigure(
        (0, 1),
        weight=1,
        uniform="assignment_form_columns",
    )

    course_workload_frame = ctk.CTkFrame(
        form_card,
        fg_color=colors.SURFACE_HOVER,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
        corner_radius=spacing.RADIUS_LARGE,
    )
    course_workload_frame.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(spacing.SPACE_2, spacing.CARD_PADDING),
        pady=spacing.CARD_PADDING,
    )
    course_workload_frame.grid_propagate(False)
    course_workload_frame.grid_rowconfigure((0, 1, 2, 3), weight=0)
    course_workload_frame.grid_rowconfigure(4, weight=1)
    course_workload_frame.grid_columnconfigure(
        (0, 1),
        weight=1,
        uniform="workload_stats",
    )

    form_card_label = ctk.CTkLabel(
        assignment_details_frame,
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

    top_fields_frame = ctk.CTkFrame(
        assignment_details_frame,
        fg_color=colors.TRANSPARENT,
    )
    top_fields_frame.grid(
        row=1,
        column=0,
        columnspan=2,
        sticky="ew",
    )
    top_fields_frame.grid_columnconfigure(
        (0, 1),
        weight=1,
        uniform="top_assignment_fields",
    )

    task_name_frame = ctk.CTkFrame(
        top_fields_frame,
        fg_color=colors.TRANSPARENT,
    )
    task_name_frame.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(spacing.CARD_PADDING, spacing.SPACE_2),
        pady=spacing.CARD_PADDING,
    )
    task_name_frame.grid_columnconfigure(0, weight=1)

    task_name_label = ctk.CTkLabel(
        task_name_frame,
        text="Assignment name",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    task_name_label.grid(
        row=0,
        column=0,
        sticky="w",
    )

    task_name_entry = ctk.CTkEntry(
        task_name_frame,
        font=fonts["body"],
        text_color=colors.TEXT_PRIMARY,
        placeholder_text="Enter assignment name",
        placeholder_text_color=colors.TEXT_SECONDARY,
        fg_color=colors.SURFACE,
        border_color=colors.BORDER,
        corner_radius=spacing.RADIUS_MEDIUM,
        height=38,
    )
    task_name_entry.grid(
        row=1,
        column=0,
        sticky="ew",
        pady=(spacing.SPACE_3, 0),
    )
    course_section = ctk.CTkFrame(
        top_fields_frame,
        fg_color=colors.TRANSPARENT,
    )
    course_section.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(spacing.SPACE_2, spacing.CARD_PADDING),
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
    course_dropdown = None

    if not courses:
        no_courses_label = ctk.CTkLabel(
            course_section,
            text="No active courses found.",
            font=fonts["small"],
            text_color=colors.TEXT_SECONDARY,
            justify="left",
            anchor="w",
            wraplength=280,
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

    difficulty_section = ctk.CTkFrame(
        top_fields_frame,
        fg_color=colors.TRANSPARENT,
    )
    difficulty_section.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=(spacing.CARD_PADDING, spacing.SPACE_2),
        pady=(0, spacing.CARD_PADDING),
    )
    difficulty_section.grid_columnconfigure(0, weight=1)

    difficulty_section_label = ctk.CTkLabel(
        difficulty_section,
        text="Difficulty level",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    difficulty_section_label.grid(
        row=0,
        column=0,
        sticky="w",
    )

    difficulty_section_segmented_button = ctk.CTkSegmentedButton(
        difficulty_section,
        values=["1", "2", "3", "4", "5"],
        font=fonts["body"],
        text_color=colors.TEXT_PRIMARY,
        selected_color=colors.ACCENT,
        selected_hover_color=colors.ACCENT_HOVER,
        unselected_color=colors.SURFACE_HOVER,
        unselected_hover_color=colors.BORDER,
        corner_radius=spacing.RADIUS_MEDIUM,
        height=38,
    )
    difficulty_section_segmented_button.set("3")
    difficulty_section_segmented_button.grid(
        row=1,
        column=0,
        columnspan=2,
        sticky="ew",
        pady=(spacing.SPACE_3, 0),
    )

    date_section = ctk.CTkFrame(
        top_fields_frame,
        fg_color=colors.TRANSPARENT,
    )
    date_section.grid(
        row=1,
        column=1,
        sticky="nsew",
        padx=(spacing.SPACE_2, spacing.CARD_PADDING),
        pady=(0, spacing.CARD_PADDING),
    )
    date_section.grid_columnconfigure(0, weight=1)

    date_label = ctk.CTkLabel(
        date_section,
        text="Due date",
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

    date_entry_style = ttk.Style(date_section)
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
        date_section,
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
        sticky="ew",
        pady=(spacing.SPACE_3, 0),
    )

    short_desc_section = ctk.CTkFrame(
        assignment_details_frame,
        fg_color=colors.TRANSPARENT,
    )
    short_desc_section.grid(
        row=2,
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
        assignment_details_frame,
        fg_color=colors.TRANSPARENT,
    )
    tags_section.grid(
        row=3,
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

    tags_entry = ctk.CTkEntry(
        tags_section,
        placeholder_text="e.g. Essay, Midterm, Group project",
        font=fonts["body"],
        text_color=colors.TEXT_PRIMARY,
        placeholder_text_color=colors.TEXT_SECONDARY,
        fg_color=colors.SURFACE_HOVER,
        border_color=colors.BORDER,
        corner_radius=spacing.RADIUS_MEDIUM,
        height=38,
    )
    tags_entry.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=(0, spacing.SPACE_2),
        pady=(spacing.SPACE_2, 0),
    )

    selected_tags = []
    tags_list_frame = ctk.CTkFrame(
        tags_section,
        fg_color=colors.TRANSPARENT,
    )
    tags_list_frame.grid(
        row=2,
        column=0,
        columnspan=2,
        sticky="ew",
        pady=(spacing.SPACE_2, 0),
    )
    tags_list_frame.grid_columnconfigure((0, 1, 2), weight=0)
    tags_list_frame.grid_remove()

    def render_tags():
        for widget in tags_list_frame.winfo_children():
            widget.destroy()

        if not selected_tags:
            tags_list_frame.grid_remove()
            return

        tags_list_frame.grid()

        for index, tag in enumerate(selected_tags):
            tag_text = f"#{tag}  ×"
            tag_button = ctk.CTkButton(
                tags_list_frame,
                text=tag_text,
                font=fonts["small"],
                text_color=colors.TEXT_ON_ACCENT,
                fg_color=colors.ACCENT,
                hover_color=colors.ACCENT_HOVER,
                corner_radius=spacing.RADIUS_MEDIUM,
                cursor="hand2",
                height=30,
                width=max(
                    48,
                    fonts["small"].measure(tag_text)
                    + (2 * spacing.SPACE_3),

                ),
                command=lambda value=tag: remove_tag(value),
            )
            tag_button.grid(
                row=index // 3,
                column=index % 3,
                sticky="w",
                padx=(
                    0 if index % 3 == 0 else spacing.SPACE_1,
                    0 if index % 3 == 2 else spacing.SPACE_1,
                ),
                pady=(0, spacing.SPACE_1),
            )

    def remove_tag(tag):
        selected_tags.remove(tag)
        render_tags()

    def add_tag():
        tag = tags_entry.get().strip().lstrip("#").strip()
        if not tag:
            return

        if any(existing.casefold() == tag.casefold() for existing in selected_tags):
            tags_entry.delete(0, "end")
            return

        selected_tags.append(tag)
        tags_entry.delete(0, "end")
        render_tags()

    tags_button = ctk.CTkButton(
        tags_section,
        text="Add tag",
        font=fonts["body_bold"],
        text_color=colors.TEXT_ON_ACCENT,
        fg_color=colors.ACCENT,
        hover_color=colors.ACCENT_HOVER,
        corner_radius=spacing.RADIUS_MEDIUM,
        height=38,
        width=96,
        command=add_tag,
    )
    tags_button.grid(
        row=1,
        column=1,
        sticky="e",
        pady=(spacing.SPACE_2, 0),
    )
    tags_button.configure(cursor="hand2")
    tags_entry.bind("<Return>", lambda event: add_tag())
    details_row = ctk.CTkFrame(
        assignment_details_frame,
        fg_color=colors.TRANSPARENT,
    )
    details_row.grid(
        row=4,
        column=0,
        columnspan=2,
        sticky="ew",
        padx=spacing.CARD_PADDING,
        pady=(0, spacing.CARD_PADDING),
    )
    details_row.grid_columnconfigure(
        (0, 1),
        weight=1,
        uniform="assignment_details",
    )

    hours_label = ctk.CTkLabel(
        details_row,
        text="Estimated hours",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    hours_label.grid(
        row=0,
        column=0,
        sticky="w",
    )

    hours_entry = ctk.CTkComboBox(
        details_row,
        values=["0", "1", "2", "3", "4", "5", "6", "7", "8"],
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
    hours_entry.set("0")
    hours_entry.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=(0, spacing.SPACE_2),
        pady=(spacing.SPACE_2, 0),
    )

    hours_helper = ctk.CTkLabel(
        details_row,
        text="How much work is still needed?",
        font=fonts["small"],
        text_color=colors.TEXT_SECONDARY,
    )
    hours_helper.grid(
        row=2,
        column=0,
        sticky="w",
        pady=(spacing.SPACE_1, 0),
    )

    status_label = ctk.CTkLabel(
        details_row,
        text="Assignment status",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    status_label.grid(
        row=0,
        column=1,
        sticky="w",
        padx=(spacing.SPACE_2, 0),
    )

    status_value = ctk.StringVar(value="Not Started")

    def update_status_fields(selected_status):
        if selected_status == "Completed":
            date_label.configure(text="Completion date")
            hours_label.configure(text="Total hours spent")
            hours_helper.configure(text="Your best estimate is fine.")
        else:
            date_label.configure(text="Due date")
            hours_label.configure(text="Estimated hours remaining")
            hours_helper.configure(text="How much work is still needed?")

    status_control = ctk.CTkOptionMenu(
        details_row,
        values=["Not Started", "In Progress", "Completed"],
        variable=status_value,
        command=update_status_fields,
        font=fonts["body"],
        text_color=colors.TEXT_PRIMARY,
        fg_color=colors.SURFACE,
        button_color=colors.ACCENT,
        button_hover_color=colors.ACCENT_HOVER,
        dropdown_fg_color=colors.SURFACE,
        dropdown_hover_color=colors.SURFACE_HOVER,
        dropdown_text_color=colors.TEXT_PRIMARY,
        corner_radius=spacing.RADIUS_MEDIUM,
        height=38,
    )
    status_control.grid(
        row=1,
        column=1,
        sticky="ew",
        padx=(spacing.SPACE_2, 0),
        pady=(spacing.SPACE_2, 0),
    )
    update_status_fields(status_value.get())

    course_workload_label = ctk.CTkLabel(
        course_workload_frame,
        text="Course Workload",
        font=fonts["card_title"],
        text_color=colors.TEXT_PRIMARY,
    )
    course_workload_label.grid(
        row=0,
        column=0,
        sticky="w",
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_2),
    )

    course_workload_subtitle = ctk.CTkLabel(
        course_workload_frame,
        text="Select a course to view its workload distribution.",
        font=fonts["body"],
        text_color=colors.TEXT_SECONDARY,
        anchor="w",
        justify="left",
        wraplength=250,
    )
    course_workload_subtitle.grid(
        row=1,
        column=0,
        columnspan=2,
        sticky="w",
        padx=spacing.CARD_PADDING,
        pady=(0, spacing.SPACE_2),
    )

    active_task_label_frame = ctk.CTkFrame(
        course_workload_frame,
        width=120,
        height=120,
        fg_color=colors.SURFACE_HOVER,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
        corner_radius=spacing.RADIUS_LARGE,
    )
    active_task_label_frame.grid(
        row=2,
        column=0,
        sticky="n",
        padx=(spacing.CARD_PADDING, spacing.SPACE_2),
        pady=(0, spacing.CARD_PADDING),
    )
    active_task_label_frame.grid_columnconfigure(0, weight=1)
    active_task_label_frame.grid_rowconfigure(1, weight=1)
    active_task_label_frame.grid_propagate(False)

    active_task_label = ctk.CTkLabel(
        active_task_label_frame,
        text="Active tasks",
        font=fonts["body"],
        text_color=colors.TEXT_SECONDARY,
    )
    active_task_label.grid(
        row=0,
        column=0,
        sticky="w",
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_2),
    )

    active_task_number_label = ctk.CTkLabel(
        active_task_label_frame,
        text="0",
        font=fonts["display"],
        text_color=colors.TEXT_PRIMARY,
    )

    active_task_number_label.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=spacing.CARD_PADDING,
        pady=(spacing.SPACE_2, spacing.CARD_PADDING),
    )

    hours_left_label_frame = ctk.CTkFrame(
        course_workload_frame,
        width=120,
        height=120,
        fg_color=colors.SURFACE_HOVER,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
        corner_radius=spacing.RADIUS_LARGE,
    )
    hours_left_label_frame.grid(
        row=2,
        column=1,
        sticky="n",
        padx=(spacing.SPACE_2, spacing.CARD_PADDING),
        pady=(0, spacing.CARD_PADDING),
    )
    hours_left_label_frame.grid_columnconfigure(0, weight=1)
    hours_left_label_frame.grid_rowconfigure(1, weight=1)
    hours_left_label_frame.grid_propagate(False)

    hours_left_label = ctk.CTkLabel(
        hours_left_label_frame,
        text="Hours Left",
        font=fonts["body"],
        text_color=colors.TEXT_SECONDARY,
    )
    hours_left_label.grid(
        row=0,
        column=0,
        sticky="w",
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_2),
    )

    hours_left_number_label = ctk.CTkLabel(
        hours_left_label_frame,
        text="0",
        font=fonts["display"],
        text_color=colors.TEXT_PRIMARY,
    )

    hours_left_number_label.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=spacing.CARD_PADDING,
        pady=(spacing.SPACE_2, spacing.CARD_PADDING),
    )

    def resize_workload_stat_cards(event=None):
        frame_width = course_workload_frame.winfo_width()

        if frame_width <= 1:
            course_workload_frame.after(
                20,
                resize_workload_stat_cards,
            )
            return

        horizontal_padding = (
            (2 * spacing.CARD_PADDING)
            + (2 * spacing.SPACE_2)
        )
        card_size = min(
            180,
            max(
                104,
                (frame_width - horizontal_padding) // 2,
            ),
        )
        active_task_label_frame.configure(
            width=card_size,
            height=card_size,
        )
        hours_left_label_frame.configure(
            width=card_size,
            height=card_size,
        )

    course_workload_frame.bind(
        "<Configure>",
        resize_workload_stat_cards,
        add=True,
    )
    course_workload_frame.after_idle(resize_workload_stat_cards)

    seperator = ctk.CTkFrame(
        course_workload_frame,
        fg_color=colors.BORDER,
        height=1,
    )
    seperator.grid(
        row=3,
        column=0,
        columnspan=2,
        sticky="ew",
        padx=spacing.CARD_PADDING,
        pady=(0, spacing.CARD_PADDING),
    )

    upcoming_in_this_course_label_frame = ctk.CTkFrame(
        course_workload_frame,
        fg_color=colors.SURFACE_HOVER,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
        corner_radius=spacing.RADIUS_LARGE,
    )
    upcoming_in_this_course_label_frame.grid(
        row=4,
        column=0,
        columnspan=2,
        sticky="nsew",
        padx=spacing.CARD_PADDING,
        pady=(0, spacing.CARD_PADDING),
    )
    upcoming_in_this_course_label_frame.grid_columnconfigure(0, weight=1)

    upcoming_in_this_course_label = ctk.CTkLabel(
        upcoming_in_this_course_label_frame,
        text="Upcoming in this course",
        font=fonts["body"],
        text_color=colors.TEXT_SECONDARY,
    )
    upcoming_in_this_course_label.grid(
        row=0,
        column=0,
        sticky="w",
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_2),
    )

    upcoming_tasks_list_frame = ctk.CTkFrame(
        upcoming_in_this_course_label_frame,
        fg_color=colors.TRANSPARENT,
    )
    upcoming_tasks_list_frame.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=spacing.CARD_PADDING,
        pady=(0, spacing.CARD_PADDING),
    )
    upcoming_tasks_list_frame.grid_columnconfigure(0, weight=1)

    def refresh_course_workload(course_name):
        tasks = (
            task_queries.get_tasks_by_course(course_name, get_current_user_id())
            if course_name
            else []
        )
        active_tasks = [
            task for task in tasks
            if not task_rules.is_completed(task)
        ]
        hours_left = sum(
            task_rules.remaining_hours(task)
            for task in active_tasks
        )
        future_tasks = [
            task for task in tasks
            if task.get("due_date") is not None
            and task_service.get_due_state(task["due_date"]) != "overdue"
        ]
        upcoming_tasks = task_service.select_upcoming_tasks(
            future_tasks,
            limit=3,
        )

        active_task_number_label.configure(text=str(len(active_tasks)))
        hours_left_number_label.configure(text=f"{hours_left:g}")

        for widget in upcoming_tasks_list_frame.winfo_children():
            widget.destroy()

        if not upcoming_tasks:
            empty_upcoming_label = ctk.CTkLabel(
                upcoming_tasks_list_frame,
                text="No upcoming tasks for this course.",
                font=fonts["small"],
                text_color=colors.TEXT_SECONDARY,
            )
            empty_upcoming_label.grid(row=0, column=0, sticky="w")
            return

        for row, task in enumerate(upcoming_tasks):
            task_name_label = ctk.CTkLabel(
                upcoming_tasks_list_frame,
                text=task["task"],
                font=fonts["body_bold"],
                text_color=colors.TEXT_PRIMARY,
                anchor="w",
            )
            task_name_label.grid(
                row=row,
                column=0,
                sticky="ew",
                pady=(0, spacing.SPACE_2),
            )

            due_date_label = ctk.CTkLabel(
                upcoming_tasks_list_frame,
                text=str(task["due_date"]),
                font=fonts["small"],
                text_color=colors.TEXT_SECONDARY,
                anchor="e",
            )
            due_date_label.grid(
                row=row,
                column=1,
                sticky="e",
                padx=(spacing.SPACE_2, 0),
                pady=(0, spacing.SPACE_2),
            )

    if course_dropdown is None:
        course_workload_subtitle.configure(
            text="Add an active course to view its workload distribution.",
        )
        refresh_course_workload(None)
    else:
        course_dropdown.configure(command=refresh_course_workload)
        refresh_course_workload(course_dropdown.get())

    enable_linux_mousewheel(assignment_details_frame)

def back_to_assignments(parent, fonts):
    from gui_logic.assignments import assignments_screen
    parent.winfo_toplevel().minsize(1024, 700)
    assignments_screen(parent, fonts)

def get_courses_for_user(user_id):
    courses = course_service.get_active_courses(user_id)
    return [course["course_name"] for course in courses]

def get_tasks_for_course(course_name, user_id):
    tasks = task_queries.get_tasks_by_course(course_name, user_id)
    return tasks
