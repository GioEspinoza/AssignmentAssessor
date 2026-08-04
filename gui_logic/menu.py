import customtkinter as ctk
from datetime import datetime
from PIL import Image
from backend import session, task_service
from gui_style import colors, spacing
from gui_style.responsive import ResponsiveText
from gui_widgets.dashboard_card import DashboardCard
from gui_logic import add_task, assignments, urgent_screen

# Presentation data only. A future card widget can iterate over this collection.
DASHBOARD_CARD_CONFIG = (
    {
        "key": "assignments",
        "title": "Assignments",
        "description": "Create a new assignment and set its due date. Manage your coursework and deadlines.",
        "accent_color": colors.ASSIGNMENTS_ACCENT,
        "icon": "✓",
    },
    {
        "key": "urgent",
        "title": "Urgent",
        "description": "Review assignments and their completion status. Focus on overdue and approaching work.",
        "accent_color": colors.URGENT_ACCENT,
        "icon": "!",
    },
    {
        "key": "calendar",
        "title": "Calendar",
        "description": "View your assignments and events in a monthly calendar.",
        "accent_color": colors.CALENDAR_ACCENT,
        "icon": "▦",
    },
    {
        "key": "study_planner",
        "title": "Study planner",
        "description": "Build and manage your study schedule.",
        "accent_color": colors.PLANNER_ACCENT,
        "icon": "✎",
    },
    {
        "key": "analytics",
        "title": "Analytics",
        "description": "View your progress and performance metrics.",
        "accent_color": colors.ANALYTICS_ACCENT,
        "icon": "↗",
    },
    {
        "key": "lock_in",
        "title": "Lock-in",
        "description": "Start a focused study session.",
        "accent_color": colors.LOCK_IN_ACCENT,
        "icon": "◉",
    },
)

def get_time_of_day():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def get_due_status(due_date):
    due_states = {
        "overdue": ("Overdue", colors.DANGER),
        "due_today": ("Due today", colors.WARNING),
        "due_soon": ("Due soon", colors.WARNING),
        "upcoming": ("Upcoming", colors.ACCENT),
    }
    return due_states[task_service.get_due_state(due_date)]

def menu_screen(parent, fonts, username=None):
    if username is None:
        if session.current_user is None:
            raise RuntimeError("No user is currently logged in.")
        username = session.current_user["username"]

    dashboard_data = task_service.get_dashboard_data(
        session.get_current_user_id()
    )
    dashboard_summary = dashboard_data["summary"]

    for widget in parent.winfo_children():
        widget.destroy()

    dashboard_frame = ctk.CTkFrame(
        parent,
        fg_color=colors.TRANSPARENT
    )
    header_frame = ctk.CTkFrame(
        dashboard_frame,
        fg_color=colors.TRANSPARENT,
    )
    header_fonts = {
        "title": ctk.CTkFont(
            family=fonts["page_title"].cget("family"),
            size=fonts["page_title"].cget("size"),
            weight=fonts["page_title"].cget("weight"),
        ),
        "subtitle": ctk.CTkFont(
            family=fonts["body"].cget("family"),
            size=fonts["body"].cget("size"),
            weight=fonts["body"].cget("weight"),
        ),
    }
    setattr(
        header_frame,
        "responsive_text",
        ResponsiveText(
            header_frame,
            header_fonts,
            base_width=836,
            min_scale=0.8,
            max_scale=1.25,
        ),
    )
    title_label = ctk.CTkLabel(
        header_frame,
        text=f"{get_time_of_day()}, {username}!",
        font=header_fonts["title"],
        text_color=colors.TEXT_PRIMARY,
        fg_color=colors.TRANSPARENT
    )

    search_bar = ctk.CTkEntry(
        header_frame,
        placeholder_text="🔍  Search assignments, courses, and more...",
        font=fonts["body"],
        fg_color=colors.SURFACE,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
        corner_radius=spacing.RADIUS_MEDIUM,
        height=36,
    )

    header_actions = ctk.CTkFrame(
        header_frame,
        width=144,
        height=40,
        fg_color=colors.TRANSPARENT,
    )

    greeting_subtitle = ctk.CTkLabel(
        header_frame,
        text="Here’s what needs your attention today.",
        font=header_fonts["subtitle"],
        text_color=colors.TEXT_SECONDARY,
        fg_color=colors.TRANSPARENT
    )

    def change_appearance_mode():
        appearance_mode = "dark" if dark_light_switch.get() else "light"
        ctk.set_appearance_mode(appearance_mode)

    dark_light_switch = ctk.CTkSwitch(
        header_actions,
        text="",
        width=40,
        height=36,
        switch_width=36,
        switch_height=18,
        command=change_appearance_mode,
        fg_color=colors.BORDER,
        progress_color=colors.ACCENT,
        button_color=colors.TEXT_PRIMARY,
        button_hover_color=colors.SURFACE_HOVER,
        corner_radius=spacing.RADIUS_SMALL,
    )
    if ctk.get_appearance_mode().casefold() == "dark":
        dark_light_switch.select()
    else:
        dark_light_switch.deselect()

    notification_icon = ctk.CTkImage(
        light_image=Image.open("assets/bell_light.png"),
        dark_image=Image.open("assets/bell_dark.png"),
        size=(22, 22)
    )

    profile_icon = ctk.CTkImage(
        light_image=Image.open("assets/profile_light.png"),
        dark_image=Image.open("assets/profile_dark.png"),
        size=(22, 22)
    )

    notification_button = ctk.CTkButton(
        header_actions,
        image=notification_icon,
        text="",
        width=36,
        height=36,
        corner_radius=spacing.RADIUS_MEDIUM,
        fg_color=colors.TRANSPARENT,
        hover=False,
        cursor="hand2",
        border_width=0,
        command=lambda: print("Notification button clicked"),
    )

    profile_button = ctk.CTkButton(
        header_actions,
        image=profile_icon,
        text="",
        width=36,
        height=36,
        corner_radius=spacing.RADIUS_MEDIUM,
        fg_color=colors.TRANSPARENT,
        hover=False,
        cursor="hand2",
        border_width=0,
        command=lambda: print("Profile button clicked"),
    )

    separator = ctk.CTkFrame(
        dashboard_frame,
        height=2,
        corner_radius=0,
        fg_color=colors.DIVIDER
    )
    content_frame = ctk.CTkScrollableFrame(
        dashboard_frame,
        fg_color=colors.TRANSPARENT,
        corner_radius=0,
        scrollbar_button_color=colors.BORDER,
        scrollbar_button_hover_color=colors.TEXT_SECONDARY,
    )
    at_a_glance_label = ctk.CTkLabel(
        content_frame,
        text="At a glance",
        font=fonts["section_title"],
        text_color=colors.TEXT_PRIMARY,
        fg_color=colors.TRANSPARENT
    )
    stats_container = ctk.CTkFrame(
        content_frame,
        fg_color=colors.TRANSPARENT,
    )
    quick_actions_label = ctk.CTkLabel(
        content_frame,
        text="Quick actions",
        font=fonts["section_title"],
        text_color=colors.TEXT_PRIMARY,
        fg_color=colors.TRANSPARENT
    )
    cards_container = ctk.CTkFrame(
        content_frame,
        fg_color=colors.TRANSPARENT,
    )

    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    dashboard_frame.grid(row=0, column=0, sticky='nsew')
    dashboard_frame.grid_columnconfigure(0, weight=1)
    dashboard_frame.grid_rowconfigure(2, weight=1)

    header_frame.grid(
        row=0,
        column=0,
        padx=spacing.PAGE_X,
        pady=(spacing.PAGE_Y, spacing.SPACE_4),
        sticky="ew",
    )
    header_frame.grid_columnconfigure(0, weight=1, uniform="header_sides")
    header_frame.grid_columnconfigure(1, weight=3)
    header_frame.grid_columnconfigure(2, weight=1, uniform="header_sides")
    header_actions.grid_propagate(False)
    header_actions.grid_columnconfigure((0, 1, 2), minsize=36)

    title_label.grid(
        row=0,
        column=0,
        pady=(0, spacing.SPACE_1),
        sticky="nw",
    )

    search_bar.grid(
        row=0,
        column=1,
        rowspan=2,
        padx=spacing.SPACE_4,
        sticky="ew",
    )

    dark_light_switch.grid(
        row=0,
        column=0,
        padx=(0, spacing.SPACE_2),
        pady=0,
        sticky="e",
    )

    notification_button.grid(
        row=0,
        column=1,
        padx=(0, spacing.SPACE_1),
        pady=0,
        sticky="e",
    )

    profile_button.grid(
        row=0,
        column=2,
        padx=(0, spacing.SPACE_2),
        pady=0,
        sticky="e",
    )

    greeting_subtitle.grid(
        row=1,
        column=0,
        sticky="nw",
    )

    header_actions.grid(
        row=0,
        column=2,
        rowspan=2,
        padx=(0, spacing.SPACE_2),
        sticky="e",
    )

    separator.grid(
        row=1,
        column=0,
        sticky="ew"
    )

    content_frame.grid(
        row=2,
        column=0,
        sticky="nsew",
    )
    content_frame.grid_columnconfigure(0, weight=1)

    at_a_glance_label.grid(
        row=0,
        column=0,
        padx=spacing.PAGE_X,
        pady=(spacing.SPACE_4, spacing.SPACE_2),
        sticky="nw",
    )

    stats_container.grid(
        row=1,
        column=0,
        padx=spacing.PAGE_X,
        sticky="ew"
    )
    stats_container.grid_columnconfigure(
        (0, 1, 2),
        weight=1,
        uniform="dashboard_stats",
    )

    stats = (
        (str(dashboard_summary["due_soon"]), "Due soon"),
        (str(dashboard_summary["in_progress_tasks"]), "In progress"),
        (str(dashboard_summary["completed_tasks"]), "Completed"),
    )

    for column, (count, label) in enumerate(stats):
        stat_card = ctk.CTkFrame(
            stats_container,
            height=64,
            fg_color=colors.SURFACE,
            corner_radius=spacing.RADIUS_MEDIUM,
            border_width=spacing.CARD_BORDER_WIDTH,
            border_color=colors.BORDER,
        )
        stat_card.grid_propagate(False)
        stat_card.grid_columnconfigure(1, weight=1)

        count_label = ctk.CTkLabel(
            stat_card,
            text=count,
            font=fonts["stat"],
            text_color=colors.TEXT_PRIMARY,
        )
        stat_label = ctk.CTkLabel(
            stat_card,
            text=label,
            font=fonts["small"],
            text_color=colors.TEXT_SECONDARY,
        )

        left_padding = 0 if column == 0 else spacing.SPACE_2
        right_padding = 0 if column == 2 else spacing.SPACE_2

        stat_card.grid(
            row=0,
            column=column,
            padx=(left_padding, right_padding),
            sticky="ew",
        )
        count_label.grid(
            row=0,
            column=0,
            padx=(spacing.SPACE_4, spacing.SPACE_3),
            pady=spacing.SPACE_3,
        )
        stat_label.grid(
            row=0,
            column=1,
            padx=(0, spacing.SPACE_4),
            pady=spacing.SPACE_3,
            sticky="w",
        )

    quick_actions_label.grid(
        row=2,
        column=0,
        padx=spacing.PAGE_X,
        pady=(spacing.SPACE_5, spacing.SPACE_2),
        sticky="nw",
    )

    cards_container.grid(
        row=3,
        column=0,
        padx=spacing.PAGE_X,
        pady=0,
        sticky="ew",
    )
    cards_container.grid_columnconfigure(
        (0, 1, 2),
        weight=1,
        uniform="dashboard_cards",
        )

    cards_container.grid_rowconfigure(
        (0, 1),
        weight=0,
        minsize=spacing.CARD_MIN_HEIGHT,
        uniform="dashboard_cards",
    )


    assignment_card = DashboardCard(
        cards_container,
        fonts=fonts,
        title=DASHBOARD_CARD_CONFIG[0]["title"],
        description=DASHBOARD_CARD_CONFIG[0]["description"],
        accent_color=DASHBOARD_CARD_CONFIG[0]["accent_color"],
        icon=DASHBOARD_CARD_CONFIG[0]["icon"],
        command=lambda: assignments.assignments_screen(parent, fonts)
    )

    assignment_card.grid(
        row=0,
        column=0,
        padx=(0, spacing.SPACE_3),
        pady=(0, spacing.SPACE_3),
        sticky="nsew"
    )

    urgent_card = DashboardCard(
        cards_container,
        fonts=fonts,
        title=DASHBOARD_CARD_CONFIG[1]["title"],
        description=DASHBOARD_CARD_CONFIG[1]["description"],
        accent_color=DASHBOARD_CARD_CONFIG[1]["accent_color"],
        icon=DASHBOARD_CARD_CONFIG[1]["icon"],
        command=lambda: urgent_screen.urgent_screen(parent, fonts),
    )

    urgent_card.grid(
        row=0,
        column=1,
        padx=(spacing.SPACE_3, spacing.SPACE_3),
        pady=(0, spacing.SPACE_3),
        sticky="nsew"
    )

    calendar_card = DashboardCard(
        cards_container,
        fonts=fonts,
        title=DASHBOARD_CARD_CONFIG[2]["title"],
        description=DASHBOARD_CARD_CONFIG[2]["description"],
        accent_color=DASHBOARD_CARD_CONFIG[2]["accent_color"],
        icon=DASHBOARD_CARD_CONFIG[2]["icon"],
        command=lambda: print("Calendar card clicked"),
    )

    calendar_card.grid(
        row=0,
        column=2,
        padx=(spacing.SPACE_3, 0),
        pady=(0, spacing.SPACE_3),
        sticky="nsew"
    )

    study_planner_card = DashboardCard(
        cards_container,
        fonts=fonts,
        title=DASHBOARD_CARD_CONFIG[3]["title"],
        description=DASHBOARD_CARD_CONFIG[3]["description"],
        accent_color=DASHBOARD_CARD_CONFIG[3]["accent_color"],
        icon=DASHBOARD_CARD_CONFIG[3]["icon"],
        command=lambda: print("Study planner card clicked"),
    )

    study_planner_card.grid(
        row=1,
        column=0,
        padx=(0, spacing.SPACE_3),
        pady=(spacing.SPACE_3, 0),
        sticky="nsew"
    )

    analytics_card = DashboardCard(
        cards_container,
        fonts=fonts,
        title=DASHBOARD_CARD_CONFIG[4]["title"],
        description=DASHBOARD_CARD_CONFIG[4]["description"],
        accent_color=DASHBOARD_CARD_CONFIG[4]["accent_color"],
        icon=DASHBOARD_CARD_CONFIG[4]["icon"],
        command=lambda: print("Analytics card clicked"),
    )

    analytics_card.grid(
        row=1,
        column=1,
        padx=(spacing.SPACE_3, spacing.SPACE_3),
        pady=(spacing.SPACE_3, 0),
        sticky="nsew"
    )

    lock_in_card = DashboardCard(
        cards_container,
        fonts=fonts,
        title=DASHBOARD_CARD_CONFIG[5]["title"],
        description=DASHBOARD_CARD_CONFIG[5]["description"],
        accent_color=DASHBOARD_CARD_CONFIG[5]["accent_color"],
        icon=DASHBOARD_CARD_CONFIG[5]["icon"],
        command=lambda: print("Lock-in card clicked"),
    )

    lock_in_card.grid(
        row=1,
        column=2,
        padx=(spacing.SPACE_3, 0),
        pady=(spacing.SPACE_3, 0),
        sticky="nsew"
    )

    up_next_label = ctk.CTkLabel(
        content_frame,
        text="Up next",
        font=fonts["section_title"],
        text_color=colors.TEXT_PRIMARY,
        fg_color=colors.TRANSPARENT,
    )
    up_next_panel = ctk.CTkFrame(
        content_frame,
        fg_color=colors.SURFACE,
        corner_radius=spacing.RADIUS_LARGE,
        border_width=spacing.CARD_BORDER_WIDTH,
        border_color=colors.BORDER,
    )
    up_next_accent = ctk.CTkFrame(
        up_next_panel,
        width=spacing.CARD_ACCENT_WIDTH,
        fg_color=colors.ACCENT,
        corner_radius=spacing.RADIUS_LARGE,
    )

    up_next_label.grid(
        row=4,
        column=0,
        padx=spacing.PAGE_X,
        pady=(spacing.SPACE_5, spacing.SPACE_2),
        sticky="nw",
    )
    up_next_panel.grid(
        row=5,
        column=0,
        padx=spacing.PAGE_X,
        pady=(0, spacing.PAGE_Y),
        sticky="ew",
    )
    up_next_panel.grid_columnconfigure(1, weight=1)

    upcoming_tasks = dashboard_data["upcoming_tasks"]

    if upcoming_tasks:
        last_row = len(upcoming_tasks) * 2 - 2
        up_next_accent.grid(
            row=0,
            column=0,
            rowspan=last_row + 1,
            sticky="nsw",
        )

        for index, task in enumerate(upcoming_tasks):
            row = index * 2
            task_row = ctk.CTkFrame(
                up_next_panel,
                fg_color=colors.TRANSPARENT,
                cursor="hand2",
            )
            task_row.grid_columnconfigure(0, weight=2)
            task_row.grid_columnconfigure(1, weight=1)

            task_name = ctk.CTkLabel(
                task_row,
                text=task["task"],
                font=fonts["body_bold"],
                text_color=colors.TEXT_PRIMARY,
            )
            course_name = ctk.CTkLabel(
                task_row,
                text=task["course"],
                font=fonts["small"],
                text_color=colors.TEXT_SECONDARY,
            )
            due_date = ctk.CTkLabel(
                task_row,
                text=task_service.parse_task_date(
                    task["due_date"]
                ).strftime("%b %d, %Y"),
                font=fonts["small"],
                text_color=colors.TEXT_SECONDARY,
            )
            status_text, status_color = get_due_status(task["due_date"])
            status_badge = ctk.CTkLabel(
                task_row,
                text=status_text,
                width=76,
                height=26,
                corner_radius=spacing.RADIUS_SMALL,
                font=fonts["small_bold"],
                text_color=colors.TEXT_ON_ACCENT,
                fg_color=status_color,
            )

            task_row.grid(
                row=row,
                column=1,
                padx=spacing.CARD_PADDING,
                pady=spacing.SPACE_2,
                sticky="ew",
            )
            task_name.grid(row=0, column=0, sticky="w")
            course_name.grid(row=0, column=1, padx=spacing.SPACE_3, sticky="w")
            due_date.grid(row=0, column=2, padx=spacing.SPACE_3, sticky="e")
            status_badge.grid(row=0, column=3, padx=(spacing.SPACE_3, 0), sticky="e")

            if index < len(upcoming_tasks) - 1:
                row_separator = ctk.CTkFrame(
                    up_next_panel,
                    height=1,
                    corner_radius=0,
                    fg_color=colors.DIVIDER,
                )
                row_separator.grid(
                    row=row + 1,
                    column=1,
                    padx=spacing.CARD_PADDING,
                    sticky="ew",
                )
    else:
        up_next_panel.grid_rowconfigure(1, weight=1)
        up_next_accent.grid(
            row=0,
            column=0,
            rowspan=3,
            sticky="nsw",
        )

        empty_title = ctk.CTkLabel(
            up_next_panel,
            text="You’re all caught up",
            font=fonts["card_title"],
            text_color=colors.TEXT_PRIMARY,
        )
        empty_description = ctk.CTkLabel(
            up_next_panel,
            text="Add an assignment to start building your plan.",
            font=fonts["body"],
            text_color=colors.TEXT_SECONDARY,
        )
        add_assignment_button = ctk.CTkButton(
            up_next_panel,
            text="Add assignment",
            width=128,
            height=32,
            corner_radius=spacing.RADIUS_SMALL,
            font=fonts["button"],
            fg_color=colors.ACCENT,
            hover_color=colors.ACCENT_HOVER,
            command=lambda: add_task.add_task(
                parent,
                fonts,
                back_command=lambda: menu_screen(parent, fonts),
            ),
        )

        empty_title.grid(
            row=0,
            column=1,
            padx=spacing.CARD_PADDING,
            pady=(spacing.CARD_PADDING, spacing.SPACE_1),
            sticky="w",
        )
        empty_description.grid(
            row=1,
            column=1,
            padx=spacing.CARD_PADDING,
            sticky="w",
        )
        add_assignment_button.grid(
            row=2,
            column=1,
            padx=spacing.CARD_PADDING,
            pady=(spacing.SPACE_3, spacing.CARD_PADDING),
            sticky="w",
        )


    return dashboard_frame
