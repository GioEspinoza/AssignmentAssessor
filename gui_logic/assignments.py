import customtkinter as ctk
from PIL import Image

from backend import task_service
from backend.session import get_current_user_id
from gui_style import colors, spacing
from gui_style.responsive import clone_fonts, ResponsiveText
from gui_widgets.widgets import enable_linux_mousewheel


STATUS_FILTERS = {
    'Not Started': 'not_started',
    'In Progress': 'in_progress',
    'Completed': 'completed',
}


def assignments_screen(parent, fonts):
    user_task_list = task_service.get_tasks(get_current_user_id())
    task_list = user_task_list
    base_fonts = fonts

    fonts = clone_fonts(fonts)
    fonts["empty_message"] = ctk.CTkFont(
        family=fonts["body"].cget("family"),
        size=20,
        weight="bold",
    )
    
    for widget in parent.winfo_children():
        widget.destroy()

    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    #create assignments frame
    assignments_frame = ctk.CTkFrame(
        parent,
        fg_color=colors.TRANSPARENT
    )
    assignments_frame.grid(row=0, column=0, sticky='nsew')
    assignments_frame.grid_columnconfigure(0, weight=2)
    assignments_frame.grid_columnconfigure(1, weight=1)
    assignments_frame.grid_rowconfigure(3, weight=1, uniform="detail_panels")
    assignments_frame.grid_rowconfigure(4, weight=1, uniform="detail_panels")
    setattr(
        assignments_frame,
        "responsive_text",
        ResponsiveText(
            assignments_frame,
            fonts,
            base_width=900,
            min_scale=0.8,
            max_scale=1.25,
        ),
    )

    header_frame = ctk.CTkFrame(
        assignments_frame,
        fg_color=colors.TRANSPARENT
    )
    header_frame.grid_columnconfigure(0, weight=1)
    header_frame.grid_columnconfigure(1, weight=0)
    header_frame.grid_columnconfigure(2, weight=1)
    header_frame.grid(
        row=0, 
        column=0, 
        sticky='ew', 
        padx=spacing.PAGE_X,
        pady=(spacing.PAGE_Y, spacing.SPACE_2),
        columnspan=2
        )
    
    back_button = ctk.CTkButton(
        header_frame,
        text='< Back to Menu',
        font=fonts["button"],
        fg_color=colors.ACCENT,
        hover_color=colors.ACCENT_HOVER,
        text_color=colors.TEXT_ON_ACCENT,
        corner_radius=spacing.RADIUS_MEDIUM,
        command=lambda: return_to_menu(parent, base_fonts)
    )
    back_button.grid(
        row=0,
        column=0,
        sticky='w',
        padx=(0, spacing.SPACE_2),
        pady=(0, spacing.SPACE_2),
    )
    
    title_label = ctk.CTkLabel(
        header_frame,
        text='Assignments',
        font=fonts["page_title"],
        text_color=colors.TEXT_PRIMARY,
    )
    title_label.grid(row=1, column=0, sticky='w')
    
    subtitle_label = ctk.CTkLabel(
        header_frame,
        text='View and manage your assignments',
        font=fonts["subtitle"],
        text_color=colors.TEXT_SECONDARY,
    )
    subtitle_label.grid(row=2, column=0, sticky='w', pady=(spacing.SPACE_1, 0))
    
    add_assignment_button = ctk.CTkButton(
        header_frame,
        text='Add Assignment',
        font=fonts["button"],
        fg_color=colors.ACCENT,
        hover_color=colors.ACCENT_HOVER,
        text_color=colors.TEXT_ON_ACCENT,
        corner_radius=spacing.RADIUS_MEDIUM,
        command=lambda: add_task(parent, base_fonts)
    )
    add_assignment_button.grid(
        row=0,
        column=2,
        padx=(spacing.SPACE_2, 0),
        pady=(0, spacing.SPACE_2),
        sticky='e',
    )
    
    seperator = ctk.CTkFrame(
        assignments_frame,
        height=2,
        corner_radius=0,
        fg_color=colors.DIVIDER,
    )
    seperator.grid(
        row=1, 
        column=0, 
        sticky='ew', 
        padx=spacing.PAGE_X,
        pady=(0, spacing.SECTION_GAP),
        columnspan=2
        )
    
    search_frame = ctk.CTkFrame(
        assignments_frame,
        fg_color=colors.TRANSPARENT
    )
    search_frame.grid(
        row=2,
        column=0,
        sticky='ew',
        padx=(spacing.PAGE_X, spacing.SPACE_2),
        pady=(0, spacing.SECTION_GAP),
    )
    search_frame.grid_columnconfigure(0, weight=1)
    
    search_subtitle_label = ctk.CTkLabel(
        search_frame,
        text='Search:',
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    search_subtitle_label.grid(
        row=0,
        column=0,
        sticky='w',
        padx=(0, spacing.SPACE_2),
    )
    
    search_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text='Search assignments...',
        font=fonts["input"],
        height=36,
        corner_radius=spacing.RADIUS_MEDIUM,
        fg_color=colors.SURFACE,
        border_color=colors.BORDER,
        text_color=colors.TEXT_PRIMARY,
        placeholder_text_color=colors.TEXT_SECONDARY,
    )
    search_entry.grid(row=1, column=0, sticky='ew')
    
    filter_frame = ctk.CTkFrame(
        assignments_frame,
        fg_color=colors.TRANSPARENT
    )
    filter_frame.grid_columnconfigure(0, weight=1)
    filter_frame.grid(
        row=2,
        column=1,
        sticky='ew',
        padx=(spacing.SPACE_2, spacing.PAGE_X),
        pady=(0, spacing.SECTION_GAP),
    )
    
    show_label = ctk.CTkLabel(
        filter_frame,
        text='Show:',
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    show_label.grid(
        row=0,
        column=0,
        sticky='w',
        padx=(0, spacing.SPACE_2),
    )
    
    filter_dropdown = ctk.CTkOptionMenu(
        filter_frame,
        values=['All', 'Not Started', 'In Progress', 'Completed'],
        width=1,
        font=fonts["input"],
        dropdown_font=fonts["input"],
        height=36,
        corner_radius=spacing.RADIUS_MEDIUM,
        fg_color=colors.SURFACE,
        button_color=colors.SURFACE_HOVER,
        button_hover_color=colors.BORDER,
        text_color=colors.TEXT_PRIMARY,
        dropdown_fg_color=colors.SURFACE,
        dropdown_hover_color=colors.SURFACE_HOVER,
        dropdown_text_color=colors.TEXT_PRIMARY,
        dynamic_resizing=False,
        anchor='w',
    )
    filter_dropdown.grid(row=1, column=0, sticky='ew')

    no_assignments_image = ctk.CTkImage(
        light_image=Image.open("assets/binary_dark.png"),
        dark_image=Image.open("assets/binary_light.png"),
        size=(86, 86),
    )
    side_panel_empty_image = ctk.CTkImage(
        light_image=Image.open("assets/binary_dark.png"),
        dark_image=Image.open("assets/binary_light.png"),
        size=(48, 48),
    )
    
    assignments_list_frame = ctk.CTkScrollableFrame(
        assignments_frame,
        fg_color=colors.SURFACE,
        corner_radius=spacing.RADIUS_LARGE,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
    )
    assignments_list_frame.grid(
        row=3,
        column=0,
        columnspan=1,
        rowspan=2,
        sticky='nsew',
        padx=(spacing.PAGE_X, spacing.SPACE_2),
        pady=(0, spacing.PAGE_Y),
    )
    assignments_list_frame.grid_columnconfigure(0, weight=1)
    
    assignments_list_title = ctk.CTkLabel(
        assignments_list_frame,
        text='Your Assignments:',
        font=fonts["section_title"],
        text_color=colors.TEXT_PRIMARY,
    )
    assignments_list_title.grid(
        row=0,
        column=0,
        sticky='w',
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_2),
    )
    
    assignments_list_subtitle = ctk.CTkLabel(
        assignments_list_frame,
        text=f"Total Assignments: {len(task_list)}",
        font=fonts["small"],
        text_color=colors.TEXT_SECONDARY,
    )
    assignments_list_subtitle.grid(
        row=1,
        column=0,
        sticky='w',
        padx=spacing.CARD_PADDING,
        pady=(0, spacing.CARD_PADDING),
    )
    task_row_widgets = []
    task_click_targets = []
    selection_state = {"task": None, "frame": None}
    no_search_results_label = None

    if not task_list:
        assignments_list_frame.grid_rowconfigure(2, weight=1)
        empty_state_frame = ctk.CTkFrame(
            assignments_list_frame,
            fg_color=colors.TRANSPARENT,
        )
        empty_state_frame.grid(
            row=2,
            column=0,
            sticky='nsew',
            padx=spacing.CARD_PADDING,
            pady=(spacing.SPACE_2, spacing.CARD_PADDING),
        )
        empty_state_frame.grid_columnconfigure(0, weight=1)
        empty_state_frame.grid_rowconfigure(0, weight=1)
        empty_state_frame.grid_rowconfigure(3, weight=1)
        
        no_assignments_icon = ctk.CTkLabel(
            empty_state_frame,
            image=no_assignments_image,
            text='',
        )
        no_assignments_icon.grid(
            row=1,
            column=0,
            pady=(0, spacing.SPACE_3),
        )

        no_assignments_label = ctk.CTkLabel(
            empty_state_frame,
            text='No assignments found — suspiciously peaceful.',
            font=fonts["empty_message"],
            text_color=colors.TEXT_PRIMARY,
            wraplength=spacing.CARD_MIN_WIDTH * 2,
            justify='center',
        )
        no_assignments_label.grid(
            row=2,
            column=0,
            padx=spacing.SPACE_4,
            pady=(0, spacing.SPACE_3),
        )
    else:
        for index, task in enumerate(task_list):
            task_frame = ctk.CTkFrame(
            assignments_list_frame,
            fg_color=colors.SURFACE,
            corner_radius=spacing.RADIUS_MEDIUM,
            border_width=spacing.CARD_BORDER_WIDTH,
            border_color=colors.BORDER,
            cursor='hand2'
            )
            task_frame.grid(
                row=index + 2,
                column=0,
                sticky='ew',
                padx=spacing.CARD_PADDING,
                pady=(0, spacing.SPACE_1),
            )
            task_frame.grid_columnconfigure(0, weight=1)
            task_row_widgets.append((task, task_frame))
            
            task_title_label = ctk.CTkLabel(
                task_frame,
                text=task['task'],
                font=fonts["body_bold"],
                text_color=colors.TEXT_PRIMARY,
            )
            task_title_label.grid(row=0, column=0, sticky='w', padx=(spacing.SPACE_2, 0), pady=(spacing.SPACE_1, 0))
            
            task_due_date_label = ctk.CTkLabel(
                task_frame,
                text=f"Due: {task['due_date']}",
                font=fonts["small"],
                text_color=colors.TEXT_SECONDARY,
            )
            task_due_date_label.grid(row=1, column=0, sticky='w', padx=(spacing.SPACE_2, 0), pady=(0, spacing.SPACE_1))
            task_click_targets.append(
                (task, task_frame, (task_frame, task_title_label, task_due_date_label))
            )

        no_search_results_label = ctk.CTkLabel(
            assignments_list_frame,
            text='No assignments match your search.',
            font=fonts["body_bold"],
            text_color=colors.TEXT_SECONDARY,
        )
        no_search_results_label.grid(
            row=2,
            column=0,
            sticky='nsew',
            padx=spacing.CARD_PADDING,
            pady=spacing.CARD_PADDING,
        )
        no_search_results_label.grid_remove()

    quick_view_frame = ctk.CTkScrollableFrame(
        assignments_frame,
        fg_color=colors.SURFACE,
        corner_radius=spacing.RADIUS_LARGE,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
    )
    quick_view_frame.grid(
        row=3,
        column=1,
        sticky='nsew',
        padx=(spacing.SPACE_2, spacing.PAGE_X),
        pady=(0, spacing.PAGE_Y),
    )
    quick_view_frame.grid_columnconfigure(0, weight=1)
    quick_view_frame.grid_rowconfigure(1, weight=1)

    quick_view_title = ctk.CTkLabel(
        quick_view_frame,
        text='Quick View',
        font=fonts["section_title"],
        text_color=colors.TEXT_PRIMARY,
    )
    quick_view_title.grid(
        row=0,
        column=0,
        sticky='w',
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_2),
    )
    quick_view_content = ctk.CTkFrame(
        quick_view_frame,
        fg_color=colors.TRANSPARENT,
    )
    quick_view_content.grid(
        row=1,
        column=0,
        sticky='nsew',
        padx=spacing.CARD_PADDING,
        pady=(0, spacing.CARD_PADDING),
    )
    quick_view_content.grid_columnconfigure(0, weight=1)

    def update_quick_view(task=None):
        for widget in quick_view_content.winfo_children():
            widget.destroy()

        for row in range(7):
            quick_view_content.grid_rowconfigure(row, weight=0)

        if task is None:
            quick_view_content.grid_rowconfigure(0, weight=1)
            quick_view_content.grid_rowconfigure(3, weight=1)

            quick_view_empty_icon = ctk.CTkLabel(
                quick_view_content,
                image=side_panel_empty_image,
                text='',
            )
            quick_view_empty_icon.grid(
                row=1,
                column=0,
                pady=(0, spacing.SPACE_2),
            )

            quick_view_subtitle = ctk.CTkLabel(
                quick_view_content,
                text='Select an assignment to view its details.',
                font=fonts["body"],
                text_color=colors.TEXT_SECONDARY,
                wraplength=spacing.CARD_MIN_WIDTH - 2 * spacing.CARD_PADDING,
                justify='center',
            )
            quick_view_subtitle.grid(
                row=2,
                column=0,
                padx=spacing.SPACE_2,
                pady=(0, spacing.SPACE_2),
            )
            return

        status = task.get("status", "not_started")
        status_text = get_status_label(status)
        status_color = get_status_color(status)
        completed = status == "completed"
        date_text = task.get("date_completed") if completed else task.get("due_date")
        date_label = "Completed" if completed else "Due"

        detail_rows = (
            (task.get("task", "Untitled assignment"), fonts["card_title"], colors.TEXT_PRIMARY),
            (task.get("course", "No course"), fonts["body"], colors.TEXT_SECONDARY),
            (status_text, fonts["body_bold"], status_color),
            (f"{date_label}: {date_text or '—'}", fonts["body"], colors.TEXT_PRIMARY),
            (get_hours_text(task), fonts["body"], colors.TEXT_PRIMARY),
            (f"Difficulty: {task.get('difficulty') or '—'}/5", fonts["body"], colors.TEXT_PRIMARY),
        )

        for row, (text, font, text_color) in enumerate(detail_rows):
            detail_label = ctk.CTkLabel(
                quick_view_content,
                text=text,
                font=font,
                text_color=text_color,
                justify='left',
                anchor='w',
            )
            detail_label.grid(
                row=row,
                column=0,
                sticky='ew',
                pady=(0, spacing.SPACE_2),
            )

    def select_task(task, selected_frame):
        previous_frame = selection_state["frame"]
        if previous_frame is not None and previous_frame.winfo_exists():
            previous_frame.configure(
                fg_color=colors.SURFACE,
                border_color=colors.BORDER,
            )

        selection_state["task"] = task
        selection_state["frame"] = selected_frame
        selected_frame.configure(
            fg_color=colors.SURFACE_HOVER,
            border_color=colors.ACCENT,
        )
        update_quick_view(task)

    update_quick_view()

    for task, task_frame, click_targets in task_click_targets:
        for widget in click_targets:
            widget.configure(cursor='hand2')
            widget.bind(
                "<Button-1>",
                lambda event, selected_task=task, selected_frame=task_frame:
                    select_task(selected_task, selected_frame),
            )
    
    at_a_glance_frame = ctk.CTkFrame(
            assignments_frame,
            fg_color=colors.SURFACE,
            corner_radius=spacing.RADIUS_LARGE,
            border_width=spacing.CARD_BORDER_WIDTH,
            border_color=colors.BORDER,
        )
    at_a_glance_frame.grid(
        row=4,
        column=1,
        sticky='nsew',
        padx=(spacing.SPACE_2, spacing.PAGE_X),
        pady=(0, spacing.PAGE_Y),
    )
    at_a_glance_frame.grid_columnconfigure(0, weight=1)
    at_a_glance_frame.grid_columnconfigure(1, weight=0)

    at_a_glance_title = ctk.CTkLabel(
        at_a_glance_frame,
        text='At a Glance',
        font=fonts["section_title"],
        text_color=colors.TEXT_PRIMARY,
    )
    at_a_glance_title.grid(
        row=0,
        column=0,
        sticky='w',
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_2),
    )
    if not task_list:
        at_a_glance_frame.grid_rowconfigure(1, weight=1)
        at_a_glance_empty_state_label = ctk.CTkLabel(
            at_a_glance_frame,
            image=side_panel_empty_image,
            compound='top',
            text='No assignments detected.',
            font=fonts["body_bold"],
            text_color=colors.TEXT_SECONDARY,
            wraplength=spacing.CARD_MIN_WIDTH - 2 * spacing.CARD_PADDING,
            justify='center',
            anchor='center',
        )
        at_a_glance_empty_state_label.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky='nsew',
            padx=spacing.CARD_PADDING,
            pady=(0, spacing.CARD_PADDING),
        )
    else:
        at_a_glance_data = task_service.get_task_summary(task_list)
        
        due_this_week_label = ctk.CTkLabel(
            at_a_glance_frame,
            text=f"Due this week: {at_a_glance_data['due_this_week']}",
            font=fonts["body"],
            text_color=colors.TEXT_PRIMARY,
        )
        due_this_week_label.grid(
            row=1,
            column=0,
            sticky='w',
            padx=(spacing.CARD_PADDING, spacing.SPACE_2),
            pady=(0, spacing.CARD_PADDING),
        )
        
        workload_label = ctk.CTkLabel(
            at_a_glance_frame,
            text=f"Estimated workload: {at_a_glance_data['estimated_workload']} hrs",
            font=fonts["body"],
            text_color=colors.TEXT_PRIMARY,
        )
        workload_label.grid(
            row=2,
            column=0,
            sticky='w',
            padx=(spacing.CARD_PADDING, spacing.SPACE_2),
            pady=(0, spacing.CARD_PADDING),
        )
        
        completed_tasks_label = ctk.CTkLabel(
            at_a_glance_frame,
            text=f"Completed: {at_a_glance_data['completed_tasks']}",
            font=fonts["body"],
            text_color=colors.TEXT_PRIMARY,
        )
        completed_tasks_label.grid(
            row=3,
            column=0,
            sticky='w',
            padx=(spacing.CARD_PADDING, spacing.SPACE_2),
            pady=(0, spacing.CARD_PADDING),
        )

        view_calendar_button = ctk.CTkButton(
            at_a_glance_frame,
            text='View Calendar ->',
            font=fonts["button"],
            fg_color=colors.ACCENT,
            hover_color=colors.ACCENT_HOVER,
            text_color=colors.TEXT_ON_ACCENT,
            corner_radius=spacing.RADIUS_MEDIUM,
            command=lambda: print("View Calendar button clicked")
        )
        view_calendar_button.grid(
            row=1,
            column=1,
            sticky='e',
            padx=(0, spacing.CARD_PADDING),
            pady=(0, spacing.CARD_PADDING),
        )
        
    def apply_list_controls():
        selected_status = STATUS_FILTERS.get(filter_dropdown.get())
        filtered_tasks = task_service.filter_tasks_by_status(
            user_task_list,
            selected_status,
        )
        visible_tasks = task_service.search_tasks(
            filtered_tasks,
            search_entry.get(),
        )
        visible_ids = {task["task_id"] for task in visible_tasks}

        for task, task_frame in task_row_widgets:
            if task["task_id"] in visible_ids:
                task_frame.grid()
            else:
                task_frame.grid_remove()

        selected_task = selection_state["task"]
        if (
            selected_task is not None
            and selected_task["task_id"] not in visible_ids
        ):
            selected_frame = selection_state["frame"]
            if selected_frame is not None and selected_frame.winfo_exists():
                selected_frame.configure(
                    fg_color=colors.SURFACE,
                    border_color=colors.BORDER,
                )
            selection_state["task"] = None
            selection_state["frame"] = None
            update_quick_view()

        assignments_list_subtitle.configure(
            text=f"Total Assignments: {len(visible_tasks)}"
        )

        if no_search_results_label is not None:
            if visible_tasks:
                no_search_results_label.grid_remove()
            else:
                no_search_results_label.grid()

    search_entry.bind("<KeyRelease>", lambda event: apply_list_controls())
    filter_dropdown.configure(command=lambda selected: apply_list_controls())
    enable_linux_mousewheel(assignments_frame)
    enable_linux_mousewheel(quick_view_frame)


def update_quick_view(task):
    task_details = (
        f"Task: {task['task']}\n"
        f"Status: {get_status_label(task.get('status'))}\n"
        f"Due Date: {task.get('due_date')}\n"
        f"Estimated Time: {task.get('estimated_hours', 'N/A')} hrs"
    )
    return task_details

def get_status_label(status):
    status_labels = {
        'not_started': 'Not Started',
        'in_progress': 'In Progress',
        'completed': 'Completed',
    }
    return status_labels.get(status, 'Not Started')

def get_status_color(status):
    status_colors = {
        'not_started': colors.WARNING,
        'in_progress': colors.ACCENT,
        'completed': colors.SUCCESS,
    }
    return status_colors.get(status, colors.WARNING)

def get_hours_text(task):
    if task.get('status') == 'completed':
        return f"Hours used: {task.get('hours_used') or '—'}"

    if task.get('status') == 'in_progress':
        hours_used = task.get('hours_used') or 0
        estimated_hours = task.get('estimated_hours') or '—'
        return f"Hours: {hours_used} used / {estimated_hours} estimated"

    return f"Estimated hours: {task.get('estimated_hours') or '—'}"

def return_to_menu(parents, fonts):
    from gui_logic.menu import menu_screen
    menu_screen(parents, fonts)

def add_task(parent, fonts):
    from gui_logic.add_task import add_task
    add_task(parent, fonts)
