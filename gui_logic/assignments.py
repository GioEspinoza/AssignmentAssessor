from functools import partial
from tkinter import TclError, messagebox

import customtkinter as ctk
from PIL import Image

from backend import tag_services, task_service
from backend.session import get_current_user_id
from gui_style import colors, spacing
from gui_style.responsive import clone_fonts, ResponsiveText
from gui_widgets.widgets import create_header_action
from gui_logic.navigation import return_to_menu


STATUS_FILTERS = {
    "Not Started": "not_started",
    "In Progress": "in_progress",
    "Completed": "completed",
}

TASK_ACTION_DEFINITIONS = (
    ("view", "View Task", False),
    ("edit", "Edit Task", False),
    ("delete", "Delete Task", True),
)


def build_task_action_items(task, on_action):
    return tuple(
        {
            "action": action,
            "label": label,
            "danger": danger,
            "command": partial(on_action, action, task),
        }
        for action, label, danger in TASK_ACTION_DEFINITIONS
    )


def get_assignment_list_feedback(total_count, visible_count):
    if total_count == 0:
        return "empty"
    if visible_count == 0:
        return "no_results"
    return "end"


def build_quick_view_details(task, tags):
    description = str(task.get("short_description") or "").strip()
    task_tags = tuple(tags or ())

    return {
        "tags": task_tags,
        "tags_placeholder": None if task_tags else "No tags added.",
        "description": description or None,
        "description_placeholder": (None if description else "No description provided."),
    }


def fit_label_wraplength(label):
    try:
        rendered_width = label.winfo_width()
        if rendered_width <= 1:
            return

        logical_width = label._reverse_widget_scaling(float(rendered_width))
        current_wraplength = float(label.cget("wraplength"))
        if abs(current_wraplength - logical_width) > 1:
            label.configure(wraplength=logical_width)
    except (TclError, TypeError, ValueError):
        return


class TaskActionsMenu:
    MENU_WIDTH = 168

    def __init__(self, owner, overlay_parent, fonts, on_action):
        self.owner = owner
        self.overlay_parent = overlay_parent
        self.fonts = fonts
        self.on_action = on_action
        self.active_button = None
        self.active_task = None
        self._is_visible = False
        self._reposition_job = None
        self._binding_ids = []
        self._cleanup_complete = False

        self.menu = ctk.CTkFrame(
            overlay_parent,
            width=self.MENU_WIDTH,
            fg_color=colors.SURFACE,
            border_width=spacing.CARD_BORDER_WIDTH,
            border_color=colors.BORDER,
            corner_radius=spacing.RADIUS_MEDIUM,
        )
        self.menu.grid_columnconfigure(0, weight=1)

        self._bind_overlay_events()
        self._owner_binding_id = owner.bind(
            "<Destroy>",
            self._cleanup,
            add=True,
        )

    def toggle(self, task, anchor_button):
        if self._is_visible and self.active_button is anchor_button:
            self.hide()
            return

        self.active_task = task
        self.active_button = anchor_button
        self._render_items(task)
        self._is_visible = True
        self._schedule_reposition()

    def hide(self):
        self._is_visible = False
        self.active_button = None
        self.active_task = None

        if self._reposition_job is not None:
            try:
                self.owner.after_cancel(self._reposition_job)
            except TclError:
                pass
            self._reposition_job = None

        try:
            self.menu.place_forget()
        except TclError:
            pass

    def _render_items(self, task):
        for widget in self.menu.winfo_children():
            widget.destroy()

        for row, item in enumerate(build_task_action_items(task, self.on_action)):
            action_button = ctk.CTkButton(
                self.menu,
                text=item["label"],
                font=self.fonts["body"],
                text_color=(colors.DANGER if item["danger"] else colors.TEXT_PRIMARY),
                fg_color=colors.SURFACE,
                hover_color=colors.SURFACE_HOVER,
                corner_radius=spacing.RADIUS_SMALL,
                height=34,
                anchor="w",
                cursor="hand2",
                command=partial(self._invoke_action, item["command"]),
            )
            action_button.grid(
                row=row,
                column=0,
                sticky="ew",
                padx=spacing.SPACE_1,
                pady=(
                    (spacing.SPACE_1, 0)
                    if row == 0
                    else (
                        0,
                        spacing.SPACE_1,
                    )
                    if row == len(TASK_ACTION_DEFINITIONS) - 1
                    else 0
                ),
            )

    def _invoke_action(self, command):
        self.hide()
        command()

    def _schedule_reposition(self, _event=None):
        if not self._is_visible or self._cleanup_complete:
            return

        if self._reposition_job is not None:
            try:
                self.owner.after_cancel(self._reposition_job)
            except TclError:
                return

        try:
            self._reposition_job = self.owner.after_idle(self._position_menu)
        except TclError:
            self._reposition_job = None

    def _position_menu(self):
        self._reposition_job = None
        button = self.active_button

        try:
            button_is_mapped = (
                button is not None and button.winfo_exists() and button.winfo_ismapped()
            )
        except TclError:
            return

        if not self._is_visible or not button_is_mapped:
            self.hide()
            return

        self.overlay_parent.update_idletasks()
        self.menu.update_idletasks()

        overlay_root_x = self.overlay_parent.winfo_rootx()
        overlay_root_y = self.overlay_parent.winfo_rooty()
        overlay_width = self.overlay_parent.winfo_width()
        overlay_height = self.overlay_parent.winfo_height()

        button_x = button.winfo_rootx() - overlay_root_x
        button_top = button.winfo_rooty() - overlay_root_y
        button_width = button.winfo_width()
        button_height = button.winfo_height()
        button_right = button_x + button_width
        button_bottom = button_top + button_height

        if (
            button_right <= 0
            or button_x >= overlay_width
            or button_bottom <= 0
            or button_top >= overlay_height
        ):
            self.hide()
            return

        gap = self.menu._apply_widget_scaling(spacing.SPACE_1)
        menu_width = self.menu.winfo_reqwidth()
        menu_height = self.menu.winfo_reqheight()
        max_x = max(gap, overlay_width - menu_width - gap)
        menu_x = min(max(gap, button_right - menu_width), max_x)

        space_below = max(0, overlay_height - button_bottom - gap)
        space_above = max(0, button_top - gap)
        if space_below >= menu_height or space_below >= space_above:
            menu_y = button_bottom + gap
        else:
            menu_y = button_top - gap - menu_height

        max_y = max(gap, overlay_height - menu_height - gap)
        menu_y = min(max(gap, menu_y), max_y)
        to_logical_units = self.menu._reverse_widget_scaling

        self.menu.place(
            x=to_logical_units(float(menu_x)),
            y=to_logical_units(float(menu_y)),
        )
        self.menu.lift()

    def _bind_overlay_events(self):
        toplevel = self.overlay_parent.winfo_toplevel()
        bindings = (
            (toplevel, "<Button-1>", self._close_on_outside_click),
            (toplevel, "<Configure>", self._handle_toplevel_configure),
            (toplevel, "<MouseWheel>", self._schedule_reposition),
            (toplevel, "<Button-4>", self._schedule_reposition),
            (toplevel, "<Button-5>", self._schedule_reposition),
            (toplevel, "<B1-Motion>", self._schedule_reposition),
            (toplevel, "<ButtonRelease-1>", self._schedule_reposition),
        )

        for widget, sequence, callback in bindings:
            binding_id = widget.bind(sequence, callback, add=True)
            self._binding_ids.append((widget, sequence, binding_id))

    def _handle_toplevel_configure(self, event):
        if event.widget is self.overlay_parent.winfo_toplevel():
            self._schedule_reposition()

    def _close_on_outside_click(self, event):
        if self._is_inside(event.widget, self.menu):
            return
        if self._is_inside(event.widget, self.active_button):
            return
        self.hide()

    def _cleanup(self, _event=None):
        if self._cleanup_complete:
            return

        self._cleanup_complete = True
        self.hide()

        for widget, sequence, binding_id in self._binding_ids:
            try:
                widget.unbind(sequence, binding_id)
            except TclError:
                pass
        self._binding_ids.clear()

        try:
            self.owner.unbind("<Destroy>", self._owner_binding_id)
        except TclError:
            pass

        try:
            if self.menu.winfo_exists():
                self.menu.destroy()
        except TclError:
            pass

    @staticmethod
    def _is_inside(widget, container):
        if container is None:
            return False

        while widget is not None:
            if widget == container:
                return True
            widget = getattr(widget, "master", None)
        return False


def assignments_screen(parent, fonts):
    user_id = get_current_user_id()
    task_list = task_service.get_tasks(user_id)
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

    # create assignments frame
    assignments_frame = ctk.CTkFrame(parent, fg_color=colors.TRANSPARENT)
    assignments_frame.grid(row=0, column=0, sticky="nsew")
    assignments_frame.grid_columnconfigure(0, weight=2)
    assignments_frame.grid_columnconfigure(1, weight=1)
    assignments_frame.grid_rowconfigure(3, weight=2)
    assignments_frame.grid_rowconfigure(4, weight=1)
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

    header_frame = ctk.CTkFrame(assignments_frame, fg_color=colors.TRANSPARENT)
    header_frame.grid_columnconfigure(0, weight=1)
    header_frame.grid_columnconfigure(1, weight=0)
    header_frame.grid_columnconfigure(2, weight=1)
    header_frame.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=spacing.PAGE_X,
        pady=(spacing.PAGE_Y, spacing.SPACE_2),
        columnspan=2,
    )

    back_button = create_header_action(
        header_frame,
        text="< Back to Menu",
        font=fonts["small_bold"],
        command=lambda: return_to_menu(parent, base_fonts),
    )
    back_button.grid(
        row=0,
        column=0,
        sticky="w",
        padx=(0, spacing.SPACE_2),
        pady=(0, spacing.SPACE_2),
    )

    title_label = ctk.CTkLabel(
        header_frame,
        text="Assignments",
        font=fonts["page_title"],
        text_color=colors.TEXT_PRIMARY,
    )
    title_label.grid(row=1, column=0, sticky="w")

    subtitle_label = ctk.CTkLabel(
        header_frame,
        text="View and manage your assignments",
        font=fonts["subtitle"],
        text_color=colors.TEXT_SECONDARY,
    )
    subtitle_label.grid(row=2, column=0, sticky="w", pady=(spacing.SPACE_1, 0))

    add_assignment_button = ctk.CTkButton(
        header_frame,
        text="Add Assignment",
        font=fonts["button"],
        fg_color=colors.ACCENT,
        hover_color=colors.ACCENT_HOVER,
        text_color=colors.TEXT_ON_ACCENT,
        corner_radius=spacing.RADIUS_MEDIUM,
        command=lambda: add_task(parent, base_fonts),
    )
    add_assignment_button.grid(
        row=0,
        column=2,
        padx=(spacing.SPACE_2, 0),
        pady=(0, spacing.SPACE_2),
        sticky="e",
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
        sticky="ew",
        padx=spacing.PAGE_X,
        pady=(0, spacing.SECTION_GAP),
        columnspan=2,
    )

    search_frame = ctk.CTkFrame(assignments_frame, fg_color=colors.TRANSPARENT)
    search_frame.grid(
        row=2,
        column=0,
        sticky="ew",
        padx=(spacing.PAGE_X, spacing.SPACE_2),
        pady=(0, spacing.SECTION_GAP),
    )
    search_frame.grid_columnconfigure(0, weight=1)

    search_subtitle_label = ctk.CTkLabel(
        search_frame,
        text="Search:",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    search_subtitle_label.grid(
        row=0,
        column=0,
        sticky="w",
        padx=(0, spacing.SPACE_2),
    )

    search_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text="Search assignments...",
        font=fonts["input"],
        height=36,
        corner_radius=spacing.RADIUS_MEDIUM,
        fg_color=colors.SURFACE,
        border_color=colors.BORDER,
        text_color=colors.TEXT_PRIMARY,
        placeholder_text_color=colors.TEXT_SECONDARY,
    )
    search_entry.grid(row=1, column=0, sticky="ew")

    filter_frame = ctk.CTkFrame(assignments_frame, fg_color=colors.TRANSPARENT)
    filter_frame.grid_columnconfigure(0, weight=1)
    filter_frame.grid(
        row=2,
        column=1,
        sticky="ew",
        padx=(spacing.SPACE_2, spacing.PAGE_X),
        pady=(0, spacing.SECTION_GAP),
    )

    show_label = ctk.CTkLabel(
        filter_frame,
        text="Show:",
        font=fonts["body_bold"],
        text_color=colors.TEXT_PRIMARY,
    )
    show_label.grid(
        row=0,
        column=0,
        sticky="w",
        padx=(0, spacing.SPACE_2),
    )

    filter_dropdown = ctk.CTkOptionMenu(
        filter_frame,
        values=["All", "Not Started", "In Progress", "Completed"],
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
        anchor="w",
    )
    filter_dropdown.grid(row=1, column=0, sticky="ew")

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
        sticky="nsew",
        padx=(spacing.PAGE_X, spacing.SPACE_2),
        pady=(0, spacing.PAGE_Y),
    )
    assignments_list_frame.grid_columnconfigure(0, weight=1)

    assignments_list_title = ctk.CTkLabel(
        assignments_list_frame,
        text="Your Assignments:",
        font=fonts["section_title"],
        text_color=colors.TEXT_PRIMARY,
    )
    assignments_list_title.grid(
        row=0,
        column=0,
        sticky="w",
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
        sticky="w",
        padx=spacing.CARD_PADDING,
        pady=(0, spacing.CARD_PADDING),
    )
    task_row_widgets = []
    task_click_targets = []
    selection_state = {"task": None, "frame": None}
    no_search_results_label = None
    end_of_list_frame = None
    task_actions_menu = None

    def show_task_action_coming_soon(action, task):
        action_label = next(
            label
            for action_name, label, _danger in TASK_ACTION_DEFINITIONS
            if action_name == action
        )
        messagebox.showinfo(
            "Coming soon",
            (f"{action_label} for “{task.get('task', 'this assignment')}” is coming soon."),
            parent=parent.winfo_toplevel(),
        )

    if not task_list:
        assignments_list_frame.grid_rowconfigure(2, weight=1)
        empty_state_frame = ctk.CTkFrame(
            assignments_list_frame,
            fg_color=colors.TRANSPARENT,
        )
        empty_state_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=spacing.CARD_PADDING,
            pady=(spacing.SPACE_2, spacing.CARD_PADDING),
        )
        empty_state_frame.grid_columnconfigure(0, weight=1)
        empty_state_frame.grid_rowconfigure(0, weight=1)
        empty_state_frame.grid_rowconfigure(3, weight=1)

        no_assignments_icon = ctk.CTkLabel(
            empty_state_frame,
            image=no_assignments_image,
            text="",
        )
        no_assignments_icon.grid(
            row=1,
            column=0,
            pady=(0, spacing.SPACE_3),
        )

        no_assignments_label = ctk.CTkLabel(
            empty_state_frame,
            text="No assignments found — suspiciously peaceful.",
            font=fonts["empty_message"],
            text_color=colors.TEXT_PRIMARY,
            wraplength=spacing.CARD_MIN_WIDTH * 2,
            justify="center",
        )
        no_assignments_label.grid(
            row=2,
            column=0,
            padx=spacing.SPACE_4,
            pady=(0, spacing.SPACE_3),
        )
    else:
        task_actions_menu = TaskActionsMenu(
            assignments_frame,
            parent.winfo_toplevel(),
            fonts,
            show_task_action_coming_soon,
        )

        for index, task in enumerate(task_list):
            task_frame = ctk.CTkFrame(
                assignments_list_frame,
                fg_color=colors.SURFACE,
                corner_radius=spacing.RADIUS_MEDIUM,
                border_width=spacing.CARD_BORDER_WIDTH,
                border_color=colors.BORDER,
                cursor="hand2",
            )
            task_frame.grid(
                row=index + 2,
                column=0,
                sticky="ew",
                padx=spacing.CARD_PADDING,
                pady=(0, spacing.SPACE_1),
            )
            task_frame.grid_columnconfigure(0, weight=1)
            task_frame.grid_columnconfigure(1, weight=0)
            task_row_widgets.append((task, task_frame))

            task_title_label = ctk.CTkLabel(
                task_frame,
                text=task["task"],
                font=fonts["card_title"],
                text_color=colors.TEXT_PRIMARY,
                anchor="w",
                justify="left",
            )
            task_title_label.grid(
                row=0,
                column=0,
                sticky="ew",
                padx=(spacing.SPACE_3, spacing.SPACE_1),
                pady=(spacing.SPACE_2, spacing.SPACE_1),
            )

            task_due_date_label = ctk.CTkLabel(
                task_frame,
                text=f"Due: {task['due_date']}",
                font=fonts["body"],
                text_color=colors.TEXT_SECONDARY,
                anchor="w",
                justify="left",
            )
            task_due_date_label.grid(
                row=1,
                column=0,
                sticky="ew",
                padx=(spacing.SPACE_3, spacing.SPACE_1),
                pady=(0, spacing.SPACE_2),
            )

            task_actions_button = ctk.CTkButton(
                task_frame,
                text="⋮",
                font=fonts["card_title"],
                text_color=colors.TEXT_SECONDARY,
                fg_color=colors.SURFACE,
                hover_color=colors.SURFACE_HOVER,
                border_width=spacing.CARD_BORDER_WIDTH,
                border_color=colors.BORDER,
                corner_radius=spacing.RADIUS_MEDIUM,
                width=34,
                height=34,
                cursor="hand2",
            )
            task_actions_button.configure(
                command=partial(
                    task_actions_menu.toggle,
                    task,
                    task_actions_button,
                ),
            )
            task_actions_button.grid(
                row=0,
                column=1,
                sticky="ne",
                padx=(spacing.SPACE_1, spacing.SPACE_2),
                pady=(spacing.SPACE_2, 0),
            )

            task_title_label.bind(
                "<Configure>",
                lambda _event, label=task_title_label: fit_label_wraplength(label),
                add=True,
            )
            task_due_date_label.bind(
                "<Configure>",
                lambda _event, label=task_due_date_label: fit_label_wraplength(label),
                add=True,
            )
            task_click_targets.append(
                (task, task_frame, (task_frame, task_title_label, task_due_date_label))
            )

        end_of_list_frame = ctk.CTkFrame(
            assignments_list_frame,
            fg_color=colors.TRANSPARENT,
        )
        end_of_list_frame.grid(
            row=len(task_list) + 2,
            column=0,
            sticky="ew",
            padx=spacing.CARD_PADDING,
            pady=(spacing.SPACE_4, spacing.CARD_PADDING),
        )
        end_of_list_frame.grid_columnconfigure(0, weight=1)

        end_of_list_icon = ctk.CTkLabel(
            end_of_list_frame,
            text="✓✓",
            font=fonts["card_title"],
            text_color=colors.SUCCESS,
            fg_color=colors.SURFACE_HOVER,
            border_width=spacing.CARD_BORDER_WIDTH,
            border_color=colors.BORDER,
            corner_radius=spacing.RADIUS_LARGE,
            width=44,
            height=32,
        )
        end_of_list_icon.grid(
            row=0,
            column=0,
            pady=(0, spacing.SPACE_2),
        )

        end_of_list_label = ctk.CTkLabel(
            end_of_list_frame,
            text="You've reached the end of your assignments.",
            font=fonts["small"],
            text_color=colors.TEXT_SECONDARY,
            justify="center",
        )
        end_of_list_label.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        no_search_results_label = ctk.CTkLabel(
            assignments_list_frame,
            text="No assignments match your search.",
            font=fonts["body_bold"],
            text_color=colors.TEXT_SECONDARY,
        )
        no_search_results_label.grid(
            row=2,
            column=0,
            sticky="nsew",
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
        sticky="nsew",
        padx=(spacing.SPACE_2, spacing.PAGE_X),
        pady=(0, spacing.PAGE_Y),
    )
    quick_view_frame.grid_columnconfigure(0, weight=1)
    quick_view_frame.grid_rowconfigure(2, weight=1)

    quick_view_header = ctk.CTkFrame(
        quick_view_frame,
        fg_color=colors.TRANSPARENT,
    )
    quick_view_header.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_3),
    )
    quick_view_header.grid_columnconfigure(0, weight=1)

    quick_view_title = ctk.CTkLabel(
        quick_view_header,
        text="Quick View",
        font=fonts["section_title"],
        text_color=colors.TEXT_PRIMARY,
        anchor="w",
    )
    quick_view_title.grid(
        row=0,
        column=0,
        sticky="ew",
    )

    quick_view_divider = ctk.CTkFrame(
        quick_view_frame,
        height=1,
        corner_radius=0,
        fg_color=colors.DIVIDER,
    )
    quick_view_divider.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=spacing.CARD_PADDING,
    )

    quick_view_content = ctk.CTkFrame(
        quick_view_frame,
        fg_color=colors.TRANSPARENT,
    )
    quick_view_content.grid(
        row=2,
        column=0,
        sticky="nsew",
        padx=spacing.CARD_PADDING,
        pady=(spacing.SPACE_4, spacing.CARD_PADDING),
    )
    quick_view_content.grid_columnconfigure(0, weight=1)
    task_tags_cache = {}

    def reset_quick_view_scroll():
        try:
            quick_view_frame.update_idletasks()
            quick_view_frame._parent_canvas.yview_moveto(0)
        except TclError:
            return

    def update_quick_view(task=None, task_tags=None):
        for widget in quick_view_content.winfo_children():
            widget.destroy()

        for row in range(5):
            quick_view_content.grid_rowconfigure(row, weight=0)

        if task is None:
            quick_view_content.grid_rowconfigure(0, weight=1)
            quick_view_content.grid_rowconfigure(3, weight=1)

            quick_view_empty_icon = ctk.CTkLabel(
                quick_view_content,
                image=side_panel_empty_image,
                text="",
            )
            quick_view_empty_icon.grid(
                row=1,
                column=0,
                pady=(0, spacing.SPACE_2),
            )

            quick_view_subtitle = ctk.CTkLabel(
                quick_view_content,
                text="Select an assignment to view its details.",
                font=fonts["body"],
                text_color=colors.TEXT_SECONDARY,
                wraplength=spacing.CARD_MIN_WIDTH - 2 * spacing.CARD_PADDING,
                justify="center",
            )
            quick_view_subtitle.grid(
                row=2,
                column=0,
                padx=spacing.SPACE_2,
                pady=(0, spacing.SPACE_2),
            )
            quick_view_frame.after_idle(reset_quick_view_scroll)
            return

        status = task.get("status", "not_started")
        status_text = get_status_label(status)
        status_color = get_status_color(status)
        completed = status == "completed"
        date_text = task.get("date_completed") if completed else task.get("due_date")
        date_label = "Completed date" if completed else "Due date"
        estimated_hours = task.get("estimated_hours")
        estimated_hours_text = f"{estimated_hours} hrs" if estimated_hours is not None else "—"
        hours_used = task.get("hours_used")
        if hours_used is not None:
            estimated_hours_text += f" · {hours_used} used"

        difficulty = task.get("difficulty")
        difficulty_text = f"{difficulty}/5" if difficulty is not None else "—"
        quick_view_details = build_quick_view_details(task, task_tags)

        assignment_identity = ctk.CTkFrame(
            quick_view_content,
            fg_color=colors.TRANSPARENT,
        )
        assignment_identity.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, spacing.SPACE_4),
        )
        assignment_identity.grid_columnconfigure(0, weight=1)

        selected_assignment_title = ctk.CTkLabel(
            assignment_identity,
            text=task.get("task", "Untitled assignment"),
            font=fonts["card_title"],
            text_color=colors.TEXT_PRIMARY,
            justify="left",
            anchor="w",
        )
        selected_assignment_title.grid(
            row=0,
            column=0,
            sticky="ew",
        )
        selected_assignment_title.bind(
            "<Configure>",
            lambda _event: fit_label_wraplength(selected_assignment_title),
            add=True,
        )

        selected_assignment_course = ctk.CTkLabel(
            assignment_identity,
            text=task.get("course", "No course"),
            font=fonts["body"],
            text_color=colors.TEXT_SECONDARY,
            justify="left",
            anchor="w",
        )
        selected_assignment_course.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(spacing.SPACE_1, 0),
        )
        selected_assignment_course.bind(
            "<Configure>",
            lambda _event: fit_label_wraplength(selected_assignment_course),
            add=True,
        )

        metadata_frame = ctk.CTkFrame(
            quick_view_content,
            fg_color=colors.TRANSPARENT,
        )
        metadata_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, spacing.SPACE_4),
        )
        metadata_values = (
            ("Status", status_text, status_color),
            (date_label, str(date_text or "—"), colors.TEXT_PRIMARY),
            (
                "Estimated hours",
                estimated_hours_text,
                colors.TEXT_PRIMARY,
            ),
            ("Difficulty", difficulty_text, colors.TEXT_PRIMARY),
        )
        metadata_cards = []

        for metadata_label, metadata_value, value_color in metadata_values:
            metadata_card = ctk.CTkFrame(
                metadata_frame,
                fg_color=colors.SURFACE,
                border_width=spacing.CARD_BORDER_WIDTH,
                border_color=colors.BORDER,
                corner_radius=spacing.RADIUS_MEDIUM,
            )
            metadata_card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                metadata_card,
                text=metadata_label,
                font=fonts["small"],
                text_color=colors.TEXT_SECONDARY,
                anchor="w",
            ).grid(
                row=0,
                column=0,
                sticky="ew",
                padx=spacing.SPACE_3,
                pady=(spacing.SPACE_2, spacing.SPACE_1),
            )

            metadata_value_label = ctk.CTkLabel(
                metadata_card,
                text=metadata_value,
                font=fonts["body_bold"],
                text_color=value_color,
                justify="left",
                anchor="w",
            )
            metadata_value_label.grid(
                row=1,
                column=0,
                sticky="ew",
                padx=spacing.SPACE_3,
                pady=(0, spacing.SPACE_3),
            )
            metadata_value_label.bind(
                "<Configure>",
                lambda _event, label=metadata_value_label: fit_label_wraplength(label),
                add=True,
            )
            metadata_cards.append(metadata_card)

        metadata_layout_state = {"wide": None}

        def layout_metadata(_event=None):
            try:
                rendered_width = metadata_frame.winfo_width()
                if rendered_width <= 1:
                    metadata_frame.after_idle(layout_metadata)
                    return

                logical_width = metadata_frame._reverse_widget_scaling(float(rendered_width))
            except TclError:
                return

            wide_layout = logical_width >= 330
            if metadata_layout_state["wide"] == wide_layout:
                return
            metadata_layout_state["wide"] = wide_layout

            for card in metadata_cards:
                card.grid_forget()

            if wide_layout:
                metadata_frame.grid_columnconfigure(
                    0,
                    weight=1,
                    uniform="quick_view_metadata",
                )
                metadata_frame.grid_columnconfigure(
                    1,
                    weight=1,
                    uniform="quick_view_metadata",
                )
                for index, card in enumerate(metadata_cards):
                    row, column = divmod(index, 2)
                    card.grid(
                        row=row,
                        column=column,
                        sticky="nsew",
                        padx=((0, spacing.SPACE_1) if column == 0 else (spacing.SPACE_1, 0)),
                        pady=((0, spacing.SPACE_2) if row == 0 else 0),
                    )
            else:
                metadata_frame.grid_columnconfigure(
                    0,
                    weight=1,
                    uniform="",
                )
                metadata_frame.grid_columnconfigure(
                    1,
                    weight=0,
                    uniform="",
                )
                for row, card in enumerate(metadata_cards):
                    card.grid(
                        row=row,
                        column=0,
                        sticky="ew",
                        pady=((0, spacing.SPACE_2) if row < len(metadata_cards) - 1 else 0),
                    )

        metadata_frame.bind(
            "<Configure>",
            layout_metadata,
            add=True,
        )
        metadata_frame.after_idle(layout_metadata)

        details_frame = ctk.CTkFrame(
            quick_view_content,
            fg_color=colors.SURFACE,
            border_width=spacing.CARD_BORDER_WIDTH,
            border_color=colors.BORDER,
            corner_radius=spacing.RADIUS_MEDIUM,
        )
        details_frame.grid(
            row=2,
            column=0,
            sticky="ew",
        )
        details_frame.grid_columnconfigure(0, weight=1)

        details_title = ctk.CTkLabel(
            details_frame,
            text="Details",
            font=fonts["body_bold"],
            text_color=colors.TEXT_PRIMARY,
            anchor="w",
        )
        details_title.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=spacing.SPACE_3,
            pady=(spacing.SPACE_3, spacing.SPACE_2),
        )

        details_tags_frame = ctk.CTkFrame(
            details_frame,
            fg_color=colors.TRANSPARENT,
        )
        details_tags_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=spacing.SPACE_3,
            pady=(0, spacing.SPACE_2),
        )
        details_tags_frame.grid_columnconfigure(0, weight=1)
        tag_layout_state = {"width": None}

        def render_detail_tags(_event=None):
            try:
                available_width = details_tags_frame.winfo_width()
            except TclError:
                return

            if available_width <= 1:
                details_tags_frame.after_idle(render_detail_tags)
                return
            if tag_layout_state["width"] == available_width:
                return
            tag_layout_state["width"] = available_width

            for widget in details_tags_frame.winfo_children():
                widget.destroy()

            if quick_view_details["tags_placeholder"]:
                no_tags_label = ctk.CTkLabel(
                    details_tags_frame,
                    text=quick_view_details["tags_placeholder"],
                    font=fonts["small"],
                    text_color=colors.TEXT_SECONDARY,
                    fg_color=colors.SURFACE_HOVER,
                    border_width=spacing.CARD_BORDER_WIDTH,
                    border_color=colors.BORDER,
                    corner_radius=spacing.RADIUS_SMALL,
                    height=28,
                )
                no_tags_label.grid(
                    row=0,
                    column=0,
                    sticky="e",
                )
                return

            chip_gap = details_tags_frame._apply_widget_scaling(spacing.SPACE_1)
            chip_padding = details_tags_frame._apply_widget_scaling(spacing.SPACE_4)
            tag_rows = []
            current_row = []
            current_width = 0

            for tag in quick_view_details["tags"]:
                tag_name = str(tag.get("tag_name") or "Tag")
                requested_width = fonts["small_bold"].measure(tag_name) + chip_padding
                next_width = (
                    requested_width
                    if not current_row
                    else current_width + chip_gap + requested_width
                )

                if current_row and next_width > available_width:
                    tag_rows.append(current_row)
                    current_row = []
                    current_width = 0

                current_row.append((tag, tag_name))
                current_width = (
                    requested_width
                    if len(current_row) == 1
                    else current_width + chip_gap + requested_width
                )

            if current_row:
                tag_rows.append(current_row)

            max_chip_wraplength = max(
                1,
                details_tags_frame._reverse_widget_scaling(float(available_width))
                - spacing.SPACE_4,
            )
            for row, tags_in_row in enumerate(tag_rows):
                tag_row = ctk.CTkFrame(
                    details_tags_frame,
                    fg_color=colors.TRANSPARENT,
                )
                tag_row.grid(
                    row=row,
                    column=0,
                    sticky="e",
                    pady=((0, spacing.SPACE_1) if row < len(tag_rows) - 1 else 0),
                )

                for index, (tag, tag_name) in enumerate(tags_in_row):
                    tag_chip = ctk.CTkLabel(
                        tag_row,
                        text=tag_name,
                        font=fonts["small_bold"],
                        text_color=tag.get(
                            "color_hex",
                            colors.ACCENT,
                        ),
                        fg_color=colors.SURFACE_HOVER,
                        border_width=spacing.CARD_BORDER_WIDTH,
                        border_color=tag.get(
                            "color_hex",
                            colors.BORDER,
                        ),
                        corner_radius=spacing.RADIUS_SMALL,
                        wraplength=max_chip_wraplength,
                        justify="left",
                        height=28,
                    )
                    tag_chip.pack(
                        side="left",
                        padx=((0, spacing.SPACE_1) if index < len(tags_in_row) - 1 else 0),
                    )

        details_tags_frame.bind(
            "<Configure>",
            render_detail_tags,
            add=True,
        )
        details_tags_frame.after_idle(render_detail_tags)

        description_frame = ctk.CTkFrame(
            details_frame,
            fg_color=colors.SURFACE_HOVER,
            border_width=spacing.CARD_BORDER_WIDTH,
            border_color=colors.BORDER,
            corner_radius=spacing.RADIUS_SMALL,
        )
        description_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=spacing.SPACE_3,
            pady=(0, spacing.SPACE_3),
        )
        description_frame.grid_columnconfigure(0, weight=1)

        description_text = (
            quick_view_details["description"] or quick_view_details["description_placeholder"]
        )
        description_label = ctk.CTkLabel(
            description_frame,
            text=description_text,
            font=fonts["body"],
            text_color=(
                colors.TEXT_PRIMARY if quick_view_details["description"] else colors.TEXT_SECONDARY
            ),
            justify="left",
            anchor="w",
        )
        description_label.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=spacing.SPACE_3,
            pady=spacing.SPACE_3,
        )
        description_label.bind(
            "<Configure>",
            lambda _event: fit_label_wraplength(description_label),
            add=True,
        )
        quick_view_frame.after_idle(reset_quick_view_scroll)

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
        task_id = task["task_id"]
        if task_id not in task_tags_cache:
            inline_tags = task.get("tags")
            task_tags_cache[task_id] = (
                inline_tags
                if inline_tags is not None
                else tag_services.get_task_tags(user_id, task_id)
            )
        update_quick_view(task, task_tags_cache[task_id])

    update_quick_view()

    for task, task_frame, click_targets in task_click_targets:
        for widget in click_targets:
            widget.configure(cursor="hand2")
            widget.bind(
                "<Button-1>",
                lambda event, selected_task=task, selected_frame=task_frame: select_task(
                    selected_task, selected_frame
                ),
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
        sticky="nsew",
        padx=(spacing.SPACE_2, spacing.PAGE_X),
        pady=(0, spacing.PAGE_Y),
    )
    at_a_glance_frame.grid_columnconfigure(0, weight=1)
    at_a_glance_frame.grid_columnconfigure(1, weight=0)

    at_a_glance_title = ctk.CTkLabel(
        at_a_glance_frame,
        text="At a Glance",
        font=fonts["section_title"],
        text_color=colors.TEXT_PRIMARY,
    )
    at_a_glance_title.grid(
        row=0,
        column=0,
        sticky="w",
        padx=spacing.CARD_PADDING,
        pady=(spacing.CARD_PADDING, spacing.SPACE_2),
    )
    if not task_list:
        at_a_glance_frame.grid_rowconfigure(1, weight=1)
        at_a_glance_empty_state_label = ctk.CTkLabel(
            at_a_glance_frame,
            image=side_panel_empty_image,
            compound="top",
            text="No assignments detected.",
            font=fonts["body_bold"],
            text_color=colors.TEXT_SECONDARY,
            wraplength=spacing.CARD_MIN_WIDTH - 2 * spacing.CARD_PADDING,
            justify="center",
            anchor="center",
        )
        at_a_glance_empty_state_label.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="nsew",
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
            sticky="w",
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
            sticky="w",
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
            sticky="w",
            padx=(spacing.CARD_PADDING, spacing.SPACE_2),
            pady=(0, spacing.CARD_PADDING),
        )

        view_calendar_button = ctk.CTkButton(
            at_a_glance_frame,
            text="View Calendar ->",
            font=fonts["button"],
            fg_color=colors.ACCENT,
            hover_color=colors.ACCENT_HOVER,
            text_color=colors.TEXT_ON_ACCENT,
            corner_radius=spacing.RADIUS_MEDIUM,
            command=lambda: print("View Calendar button clicked"),
        )
        view_calendar_button.grid(
            row=1,
            column=1,
            sticky="e",
            padx=(0, spacing.CARD_PADDING),
            pady=(0, spacing.CARD_PADDING),
        )

    def apply_list_controls():
        if task_actions_menu is not None:
            task_actions_menu.hide()

        selected_status = STATUS_FILTERS.get(filter_dropdown.get())
        filtered_tasks = task_service.filter_tasks_by_status(
            task_list,
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
        if selected_task is not None and selected_task["task_id"] not in visible_ids:
            selected_frame = selection_state["frame"]
            if selected_frame is not None and selected_frame.winfo_exists():
                selected_frame.configure(
                    fg_color=colors.SURFACE,
                    border_color=colors.BORDER,
                )
            selection_state["task"] = None
            selection_state["frame"] = None
            update_quick_view()

        assignments_list_subtitle.configure(text=f"Total Assignments: {len(visible_tasks)}")

        feedback_state = get_assignment_list_feedback(
            len(task_list),
            len(visible_tasks),
        )
        if no_search_results_label is not None:
            if feedback_state == "no_results":
                no_search_results_label.grid()
            else:
                no_search_results_label.grid_remove()

        if end_of_list_frame is not None:
            if feedback_state == "end":
                end_of_list_frame.grid()
            else:
                end_of_list_frame.grid_remove()

    search_entry.bind("<KeyRelease>", lambda event: apply_list_controls())
    filter_dropdown.configure(command=lambda selected: apply_list_controls())


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
        "not_started": "Not Started",
        "in_progress": "In Progress",
        "completed": "Completed",
    }
    return status_labels.get(status, "Not Started")


def get_status_color(status):
    status_colors = {
        "not_started": colors.WARNING,
        "in_progress": colors.ACCENT,
        "completed": colors.SUCCESS,
    }
    return status_colors.get(status, colors.WARNING)


def get_hours_text(task):
    if task.get("status") == "completed":
        return f"Hours used: {task.get('hours_used') or '—'}"

    if task.get("status") == "in_progress":
        hours_used = task.get("hours_used") or 0
        estimated_hours = task.get("estimated_hours") or "—"
        return f"Hours: {hours_used} used / {estimated_hours} estimated"

    return f"Estimated hours: {task.get('estimated_hours') or '—'}"


def add_task(parent, fonts):
    from gui_logic.add_task import add_task

    add_task(parent, fonts)
