import customtkinter as ctk
from PIL import Image

from backend import task_rules, task_service
from backend.session import get_current_user_id
from gui_style import colors, spacing
from gui_style.responsive import ResponsiveText, clone_fonts
from gui_widgets.widgets import create_header_action
from gui_logic.navigation import return_to_menu


def urgent_screen(parent, fonts):
    task_list = task_service.get_tasks(get_current_user_id())
    urgent_tasks = task_rules.urgent_sort(
        [
            task
            for task in task_list
            if task_service.get_due_state(task['due_date'])
            in ["overdue", "due_today", "due_soon"]
        ]
    )
    overdue_tasks = [
        task
        for task in urgent_tasks
        if task_service.get_due_state(task['due_date']) == "overdue"
    ]
    due_today_tasks = [
        task
        for task in urgent_tasks
        if task_service.get_due_state(task['due_date']) == "due_today"
    ]
    due_this_week_tasks = [
        task
        for task in urgent_tasks
        if task_service.get_due_state(task['due_date']) == "due_soon"
    ]

    base_fonts = fonts
    fonts = clone_fonts(fonts)

    empty_state_image = ctk.CTkImage(
        light_image=Image.open("assets/binary_dark.png"),
        dark_image=Image.open("assets/binary_light.png"),
        size=(86, 86),
    )

    for widget in parent.winfo_children():
        widget.destroy()

    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    urgents_frame = ctk.CTkFrame(
        parent,
        fg_color=colors.TRANSPARENT,
    )

    urgents_frame.grid(row=0, column=0, sticky='nsew')
    urgents_frame.grid_rowconfigure(2, weight=1)
    urgents_frame.grid_columnconfigure(0, weight=2, uniform="detail_panels")
    urgents_frame.grid_columnconfigure(1, weight=1, uniform="detail_panels")
    setattr(
        urgents_frame,
        "responsive_text",
        ResponsiveText(
            urgents_frame,
            fonts,
            base_width=900,
            min_scale=0.8,
            max_scale=1.25,
        ),
    )

    header_frame = ctk.CTkFrame(
        urgents_frame,
        fg_color=colors.TRANSPARENT,
    )

    header_frame.grid_columnconfigure(0, weight=1)
    header_frame.grid_columnconfigure(1, weight=0)
    header_frame.grid_columnconfigure(2, weight=1)
    header_frame.grid(
        row=0,
        column=0,
        columnspan=2,
        sticky='ew',
        padx=spacing.PAGE_X,
        pady=(spacing.PAGE_Y, spacing.SPACE_2),
    )

    back_button = create_header_action(
        header_frame,
        text="< Back",
        font=fonts["small_bold"],
        command=lambda: return_to_menu(parent, base_fonts),
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
        text="Urgent Tasks",
        font=fonts["page_title"],
        text_color=colors.TEXT_PRIMARY,
    )
    title_label.grid(
        row=1,
        column=0,
        sticky='w',
    )

    subtitle_label = ctk.CTkLabel(
        header_frame,
        text="Tasks that need a decision made today.",
        font=fonts["subtitle"],
        text_color=colors.TEXT_SECONDARY,
    )
    subtitle_label.grid(
        row=2,
        column=0,
        sticky='w',
        pady=(spacing.SPACE_1, 0),
    )

    quick_info_frame = ctk.CTkFrame(
        urgents_frame,
        fg_color=colors.TRANSPARENT,
    )
    quick_info_frame.grid(
        row=1,
        column=0,
        columnspan=2,
        sticky='nsew',
        padx=spacing.PAGE_X,
        pady=(0, spacing.PAGE_Y),
    )
    quick_info_frame.grid_columnconfigure(0, weight=1)
    quick_info_frame.grid_columnconfigure(1, weight=1)
    quick_info_frame.grid_columnconfigure(2, weight=1)
    quick_info_frame.grid_rowconfigure(0, weight=1)

    overdue_frame = ctk.CTkFrame(
        quick_info_frame,
        fg_color=colors.SURFACE,
        corner_radius=spacing.RADIUS_LARGE,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
    )
    overdue_frame.grid(
        row=0,
        column=0,
        sticky='nsew',
        padx=(0, spacing.SPACE_2),
    )
    overdue_frame.grid_columnconfigure(0, weight=1)
    overdue_frame.grid_rowconfigure(2, weight=1)

    overdue_label = ctk.CTkLabel(
        overdue_frame,
        text="Overdue",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    overdue_label.grid(
        row=0,
        column=0,
        sticky='w',
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_1),
    )

    overdue_subtitle = ctk.CTkLabel(
        overdue_frame,
        text="Needs attention now.",
        font=fonts["small"],
        text_color=colors.TEXT_SECONDARY,
        justify='left',
        anchor='w',
    )
    overdue_subtitle.grid(
        row=1,
        column=0,
        sticky='ew',
        padx=spacing.CARD_PADDING,
        pady=(0, spacing.SPACE_2),
    )

    if not overdue_tasks:
        overdue_empty_icon = ctk.CTkLabel(
            overdue_frame,
            image=empty_state_image,
            text='',
        )
        overdue_empty_icon.grid(
            row=2,
            column=0,
            sticky='nsew',
            padx=spacing.CARD_PADDING,
            pady=(spacing.SPACE_2, spacing.CARD_PADDING),
        )
    else:
        overdue_number = ctk.CTkLabel(
            overdue_frame,
            text=str(len(overdue_tasks)),
            font=fonts["stat"],
            text_color=colors.TEXT_PRIMARY,
        )
        overdue_number.grid(
            row=2,
            column=0,
            sticky='nsew',
            padx=spacing.CARD_PADDING,
            pady=(spacing.SPACE_2, spacing.CARD_PADDING),
        )

    due_today_frame = ctk.CTkFrame(
        quick_info_frame,
        fg_color=colors.SURFACE,
        corner_radius=spacing.RADIUS_LARGE,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
    )
    due_today_frame.grid(
        row=0,
        column=1,
        sticky='nsew',
        padx=(spacing.SPACE_2, spacing.SPACE_2),
    )
    due_today_frame.grid_columnconfigure(0, weight=1)
    due_today_frame.grid_rowconfigure(2, weight=1)

    due_today_label = ctk.CTkLabel(
        due_today_frame,
        text="Due Today",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    due_today_label.grid(
        row=0,
        column=0,
        sticky='w',
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_1),
    )

    due_today_subtitle = ctk.CTkLabel(
        due_today_frame,
        text="Needs attention today.",
        font=fonts["small"],
        text_color=colors.TEXT_SECONDARY,
        justify='left',
        anchor='w',
    )
    due_today_subtitle.grid(
        row=1,
        column=0,
        sticky='ew',
        padx=spacing.CARD_PADDING,
        pady=(0, spacing.SPACE_2),
    )

    if not due_today_tasks:
        due_today_empty_icon = ctk.CTkLabel(
            due_today_frame,
            image=empty_state_image,
            text='',
        )
        due_today_empty_icon.grid(
            row=2,
            column=0,
            sticky='nsew',
            padx=spacing.CARD_PADDING,
            pady=(spacing.SPACE_2, spacing.CARD_PADDING),
        )
    else:
        due_today_number = ctk.CTkLabel(
            due_today_frame,
            text=str(len(due_today_tasks)),
            font=fonts["stat"],
            text_color=colors.TEXT_PRIMARY,
        )
        due_today_number.grid(
            row=2,
            column=0,
            sticky='nsew',
            padx=spacing.CARD_PADDING,
            pady=(spacing.SPACE_2, spacing.CARD_PADDING),
        )

    due_this_week_frame = ctk.CTkFrame(
        quick_info_frame,
        fg_color=colors.SURFACE,
        corner_radius=spacing.RADIUS_LARGE,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
    )
    due_this_week_frame.grid(
        row=0,
        column=2,
        sticky='nsew',
        padx=(spacing.SPACE_2, 0),
    )
    due_this_week_frame.grid_columnconfigure(0, weight=1)
    due_this_week_frame.grid_rowconfigure(2, weight=1)

    due_this_week_label = ctk.CTkLabel(
        due_this_week_frame,
        text="Due This Week",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    due_this_week_label.grid(
        row=0,
        column=0,
        sticky='w',
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_1),
    )

    due_this_week_subtitle = ctk.CTkLabel(
        due_this_week_frame,
        text="Needs attention this week.",
        font=fonts["small"],
        text_color=colors.TEXT_SECONDARY,
        justify='left',
        anchor='w',
    )
    due_this_week_subtitle.grid(
        row=1,
        column=0,
        sticky='ew',
        padx=spacing.CARD_PADDING,
        pady=(0, spacing.SPACE_2),
    )

    if not due_this_week_tasks:
        due_this_week_empty_icon = ctk.CTkLabel(
            due_this_week_frame,
            image=empty_state_image,
            text='',
        )
        due_this_week_empty_icon.grid(
            row=2,
            column=0,
            sticky='nsew',
            padx=spacing.CARD_PADDING,
            pady=(spacing.SPACE_2, spacing.CARD_PADDING),
        )
    else:
        due_this_week_number = ctk.CTkLabel(
            due_this_week_frame,
            text=str(len(due_this_week_tasks)),
            font=fonts["stat"],
            text_color=colors.TEXT_PRIMARY,
        )
        due_this_week_number.grid(
            row=2,
            column=0,
            sticky='nsew',
            padx=spacing.CARD_PADDING,
            pady=(spacing.SPACE_2, spacing.CARD_PADDING),
        )

    priority_queue_frame = ctk.CTkFrame(
        urgents_frame,
        fg_color=colors.SURFACE,
        corner_radius=spacing.RADIUS_LARGE,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
    )
    priority_queue_frame.grid(
        row=2,
        column=0,
        sticky='nsew',
        padx=(spacing.PAGE_X, spacing.SPACE_2),
        pady=(0, spacing.PAGE_Y),
    )
    priority_queue_frame.grid_columnconfigure(0, weight=1)
    priority_queue_frame.grid_rowconfigure(2, weight=1)

    priority_queue_title = ctk.CTkLabel(
        priority_queue_frame,
        text="Priority Queue",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    priority_queue_title.grid(
        row=0,
        column=0,
        sticky='w',
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_1),
    )

    priority_queue_helper = ctk.CTkLabel(
        priority_queue_frame,
        text="Your most urgent assignments first.",
        font=fonts["small"],
        text_color=colors.TEXT_SECONDARY,
        justify='left',
        anchor='w',
    )
    priority_queue_helper.grid(
        row=1,
        column=0,
        sticky='ew',
        padx=spacing.CARD_PADDING,
        pady=(0, spacing.SPACE_2),
    )

    due_state_labels = {
        "overdue": "Overdue",
        "due_today": "Due today",
        "due_soon": "Due this week",
    }
    due_state_colors = {
        "overdue": colors.DANGER,
        "due_today": colors.WARNING,
        "due_soon": colors.WARNING,
    }
    task_click_targets = []
    selection_state = {"task": None, "frame": None}

    if not urgent_tasks:
        priority_queue_empty_icon = ctk.CTkLabel(
            priority_queue_frame,
            image=empty_state_image,
            text='',
        )
        priority_queue_empty_icon.grid(
            row=2,
            column=0,
            sticky='nsew',
            padx=spacing.CARD_PADDING,
            pady=(spacing.SPACE_2, spacing.CARD_PADDING),
        )
    else:
        priority_queue_list_frame = ctk.CTkScrollableFrame(
            priority_queue_frame,
            fg_color=colors.TRANSPARENT,
            border_width=0,
        )
        priority_queue_list_frame.grid(
            row=2,
            column=0,
            sticky='nsew',
            padx=spacing.CARD_PADDING,
            pady=(spacing.SPACE_2, spacing.CARD_PADDING),
        )
        priority_queue_list_frame.grid_columnconfigure(0, weight=1)

        for index, task in enumerate(urgent_tasks, start=1):
            due_state = task_service.get_due_state(task['due_date'])
            remaining_hours = task_rules.remaining_hours(task)

            task_card = ctk.CTkFrame(
                priority_queue_list_frame,
                fg_color=colors.SURFACE,
                corner_radius=spacing.RADIUS_MEDIUM,
                border_width=spacing.CARD_BORDER_WIDTH,
                border_color=colors.BORDER,
            )
            task_card.grid(
                row=index - 1,
                column=0,
                sticky='ew',
                pady=(0, spacing.SPACE_2),
            )
            task_card.grid_columnconfigure(1, weight=1)

            priority_rank_label = ctk.CTkLabel(
                task_card,
                text=f"#{index}",
                font=fonts["body_bold"],
                text_color=colors.ACCENT,
            )
            priority_rank_label.grid(
                row=0,
                column=0,
                rowspan=3,
                padx=(spacing.SPACE_2, spacing.SPACE_3),
                pady=spacing.SPACE_2,
            )

            task_title_label = ctk.CTkLabel(
                task_card,
                text=task.get("task", "Untitled assignment"),
                font=fonts["body_bold"],
                text_color=colors.TEXT_PRIMARY,
                anchor='w',
            )
            task_title_label.grid(
                row=0,
                column=1,
                sticky='ew',
                pady=(spacing.SPACE_2, 0),
            )

            due_state_label = ctk.CTkLabel(
                task_card,
                text=due_state_labels[due_state],
                font=fonts["small_bold"],
                text_color=due_state_colors[due_state],
            )
            due_state_label.grid(
                row=0,
                column=2,
                sticky='e',
                padx=spacing.SPACE_2,
                pady=(spacing.SPACE_2, 0),
            )

            course_label = ctk.CTkLabel(
                task_card,
                text=task.get("course", "No course"),
                font=fonts["small"],
                text_color=colors.TEXT_SECONDARY,
                anchor='w',
            )
            course_label.grid(
                row=1,
                column=1,
                sticky='ew',
            )

            due_date_label = ctk.CTkLabel(
                task_card,
                text=f"Due: {task.get('due_date') or '—'}",
                font=fonts["small"],
                text_color=colors.TEXT_SECONDARY,
            )
            due_date_label.grid(
                row=1,
                column=2,
                sticky='e',
                padx=spacing.SPACE_2,
            )

            workload_label = ctk.CTkLabel(
                task_card,
                text=(
                    f"{remaining_hours:g} hrs remaining"
                    f" • Difficulty {task.get('difficulty') or '—'}/5"
                ),
                font=fonts["small"],
                text_color=colors.TEXT_SECONDARY,
                anchor='w',
            )
            workload_label.grid(
                row=2,
                column=1,
                columnspan=2,
                sticky='ew',
                padx=(0, spacing.SPACE_2),
                pady=(0, spacing.SPACE_2),
            )
            task_click_targets.append(
                (
                    task,
                    task_card,
                    (
                        task_card,
                        priority_rank_label,
                        task_title_label,
                        due_state_label,
                        course_label,
                        due_date_label,
                        workload_label,
                    ),
                )
            )

    urgent_task_details_frame = ctk.CTkFrame(
        urgents_frame,
        fg_color=colors.SURFACE,
        corner_radius=spacing.RADIUS_LARGE,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
    )
    urgent_task_details_frame.grid(
        row=2,
        column=1,
        sticky='nsew',
        padx=(spacing.SPACE_2, spacing.PAGE_X),
        pady=(0, spacing.PAGE_Y),
    )
    urgent_task_details_frame.grid_columnconfigure(0, weight=1)
    urgent_task_details_frame.grid_rowconfigure(1, weight=1)

    urgent_task_details_title = ctk.CTkLabel(
        urgent_task_details_frame,
        text="Task Details",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    urgent_task_details_title.grid(
        row=0,
        column=0,
        sticky='w',
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_2),
    )

    urgent_task_details_content = ctk.CTkFrame(
        urgent_task_details_frame,
        fg_color=colors.TRANSPARENT,
    )
    urgent_task_details_content.grid(
        row=1,
        column=0,
        sticky='nsew',
        padx=spacing.CARD_PADDING,
        pady=(0, spacing.CARD_PADDING),
    )
    urgent_task_details_content.grid_columnconfigure(0, weight=1)

    def update_urgent_task_details(task=None):
        for widget in urgent_task_details_content.winfo_children():
            widget.destroy()

        for row in range(7):
            urgent_task_details_content.grid_rowconfigure(row, weight=0)

        if task is None:
            urgent_task_details_content.grid_rowconfigure(0, weight=1)
            urgent_task_details_content.grid_rowconfigure(3, weight=1)

            task_details_empty_icon = ctk.CTkLabel(
                urgent_task_details_content,
                image=empty_state_image,
                text='',
            )
            task_details_empty_icon.grid(
                row=1,
                column=0,
                pady=(0, spacing.SPACE_2),
            )

            task_details_empty_message = ctk.CTkLabel(
                urgent_task_details_content,
                text="Select an urgent assignment to view its details.",
                font=fonts["small"],
                text_color=colors.TEXT_SECONDARY,
                wraplength=spacing.CARD_MIN_WIDTH,
                justify='center',
            )
            task_details_empty_message.grid(
                row=2,
                column=0,
                padx=spacing.SPACE_2,
                pady=(0, spacing.SPACE_2),
            )
            return

        due_state = task_service.get_due_state(task['due_date'])
        remaining_hours = task_rules.remaining_hours(task)
        detail_rows = (
            (
                task.get("task", "Untitled assignment"),
                fonts["card_title"],
                colors.TEXT_PRIMARY,
            ),
            (
                task.get("course", "No course"),
                fonts["body"],
                colors.TEXT_SECONDARY,
            ),
            (
                due_state_labels[due_state],
                fonts["body_bold"],
                due_state_colors[due_state],
            ),
            (
                f"Due: {task.get('due_date') or '—'}",
                fonts["body"],
                colors.TEXT_PRIMARY,
            ),
            (
                f"Remaining work: {remaining_hours:g} hrs",
                fonts["body"],
                colors.TEXT_PRIMARY,
            ),
            (
                f"Difficulty: {task.get('difficulty') or '—'}/5",
                fonts["body"],
                colors.TEXT_PRIMARY,
            ),
        )

        for row, (text, font, text_color) in enumerate(detail_rows):
            detail_label = ctk.CTkLabel(
                urgent_task_details_content,
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

    def select_urgent_task(task, selected_frame):
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
        update_urgent_task_details(task)

    update_urgent_task_details()

    for task, task_card, click_targets in task_click_targets:
        for widget in click_targets:
            widget.configure(cursor='hand2')
            widget.bind(
                "<Button-1>",
                lambda event, selected_task=task, selected_frame=task_card:
                    select_urgent_task(selected_task, selected_frame),
            )
