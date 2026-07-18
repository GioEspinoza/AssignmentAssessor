import customtkinter as ctk
from backend import session
import datetime
from gui_style import colors, spacing
from gui_widgets.dashboard_card import DashboardCard

# will show menu after authencation


# Presentation data only. A future card widget can iterate over this collection.
DASHBOARD_CARD_CONFIG = (
    {
        "key": "assignments",
        "title": "Assignments",
        "description": "Create a new assignment and set its due date. Manage your coursework and deadlines.",
        "accent_color": colors.ASSIGNMENTS_ACCENT,
    },
    {
        "key": "urgent",
        "title": "Urgent",
        "description": "Review assignments and their completion status. Focus on overdue and approaching work.",
        "accent_color": colors.URGENT_ACCENT,
    },
    {
        "key": "calendar",
        "title": "Calendar",
        "description": "View your assignments and events in a monthly calendar.",
        "accent_color": colors.CALENDAR_ACCENT,
    },
    {
        "key": "study_planner",
        "title": "Study planner",
        "description": "Build and manage your study schedule.",
        "accent_color": colors.PLANNER_ACCENT,
    },
    {
        "key": "analytics",
        "title": "Analytics",
        "description": "View your progress and performance metrics.",
        "accent_color": colors.ANALYTICS_ACCENT,
    },
    {
        "key": "lock_in",
        "title": "Lock-in",
        "description": "Start a focused study session.",
        "accent_color": colors.LOCK_IN_ACCENT,
    },
)

def get_time_of_day():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def menu_screen(parent, fonts, username=None):
    if username is None:
        if session.current_user is None:
            raise RuntimeError("No user is currently logged in.")
        username = session.current_user["username"]

    for widget in parent.winfo_children():
        widget.destroy()

    dashboard_frame = ctk.CTkFrame(
        parent,
        fg_color=colors.TRANSPARENT
    )
    title_label = ctk.CTkLabel(
        dashboard_frame,
        text=f"{get_time_of_day()}, {username}!",
        font=fonts["display"],
        fg_color=colors.TRANSPARENT
    )
    separator = ctk.CTkFrame(
        dashboard_frame,
        height=2,
        corner_radius=0,
        fg_color=colors.DIVIDER
    )
    subtitle_label = ctk.CTkLabel(
        dashboard_frame,
        text="Dashboard",
        font=fonts["subtitle"],
        text_color=colors.TEXT_SECONDARY,
        fg_color=colors.TRANSPARENT
    )
    cards_container = ctk.CTkFrame(
        dashboard_frame,
        fg_color=colors.TRANSPARENT,
    )

    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    dashboard_frame.grid(row=0, column=0, sticky='nsew')
    dashboard_frame.grid_rowconfigure((0, 1, 2), weight=0)
    dashboard_frame.grid_rowconfigure(3, weight=1)
    dashboard_frame.grid_columnconfigure(0, weight=1)

    title_label.grid(
        row=0,
        column=0,
        padx=spacing.PAGE_X,
        pady=(spacing.PAGE_Y, spacing.SPACE_3),
        sticky="nw",
    )

    separator.grid(
        row=1,
        column=0,
        sticky="ew"
    )

    subtitle_label.grid(
        row=2,
        column=0,
        padx=spacing.PAGE_X,
        pady=(spacing.SPACE_3, spacing.SPACE_5),
        sticky="nw",
    )
    cards_container.grid(
        row=3,
        column=0,
        padx=spacing.PAGE_X,
        pady=(0, spacing.PAGE_Y),
        sticky="nsew",
    )
    cards_container.grid_columnconfigure(
        (0, 1, 2),
        weight=1,
        uniform="dashboard_cards",
        )

    cards_container.grid_rowconfigure(
        (0, 1),
        weight=1,
        uniform="dashboard_cards",
    )

    assignment_card = DashboardCard(
        cards_container,
        fonts=fonts,
        title=DASHBOARD_CARD_CONFIG[0]["title"],
        description=DASHBOARD_CARD_CONFIG[0]["description"],
        accent_color=DASHBOARD_CARD_CONFIG[0]["accent_color"],
        command=lambda: print("Assignments card clicked"),
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
        command=lambda: print("Urgent card clicked"),
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
        command=lambda: print("Lock-in card clicked"),
    )

    lock_in_card.grid(
        row=1,
        column=2,
        padx=(spacing.SPACE_3, 0),
        pady=(spacing.SPACE_3, 0),
        sticky="nsew"
    )

    return dashboard_frame
