from tkinter import TclError

import customtkinter as ctk

from gui_style import colors, spacing


def calculate_dropdown_geometry(
    entry_top,
    entry_height,
    overlay_height,
    requested_height,
    gap,
):
    entry_bottom = entry_top + entry_height
    space_below = max(0, overlay_height - entry_bottom - gap)
    space_above = max(0, entry_top - gap)

    if space_below >= requested_height:
        side = "below"
        dropdown_height = requested_height
    elif space_above > space_below:
        side = "above"
        dropdown_height = min(requested_height, space_above)
    else:
        side = "below"
        dropdown_height = min(requested_height, space_below)

    dropdown_y = (
        entry_bottom + gap
        if side == "below"
        else entry_top - gap - dropdown_height
    )
    return side, dropdown_y, dropdown_height


class TagSelector(ctk.CTkFrame):
    DROPDOWN_HEIGHT = 210

    def __init__(
        self,
        parent,
        overlay_parent,
        fonts,
        available_tags,
        on_create_tag=None,
    ):
        super().__init__(parent, fg_color=colors.TRANSPARENT)
        self.overlay_parent = overlay_parent
        self.fonts = fonts
        self.available_tags = list(available_tags)
        self.selected_tags = []
        self.on_create_tag = on_create_tag
        self._dropdown_visible = False
        self._reposition_job = None
        self._binding_ids = []
        self._cleanup_complete = False

        self.search_value = ctk.StringVar()
        self.search_value.trace_add("write", self._filter_tags)

        self.grid_columnconfigure(0, weight=1)
        self._build_selector()
        self._build_dropdown()
        self._render_selected_tags()
        self._render_preset_tags()

        self.search_entry.bind("<Button-1>", self._show_dropdown, add=True)
        self.search_entry.bind("<FocusIn>", self._show_dropdown)
        self.search_entry.bind(
            "<Configure>",
            self._schedule_reposition,
            add=True,
        )
        self.bind("<Configure>", self._schedule_reposition, add=True)
        self._bind_overlay_events()
        self.bind("<Destroy>", self._cleanup_bindings, add=True)

    def get_selected_tags(self):
        return list(self.selected_tags)

    @staticmethod
    def _normalized_tag_name(tag):
        return str(tag["tag_name"]).strip().casefold()

    def add_tag(self, tag):
        tag_name = self._normalized_tag_name(tag)
        clean_tag = {
            **tag,
            "tag_name": str(tag["tag_name"]).strip(),
        }
        self.available_tags = [
            available_tag
            for available_tag in self.available_tags
            if self._normalized_tag_name(available_tag) != tag_name
        ]
        self.available_tags.append(clean_tag)

        matching_selected_index = next(
            (
                index
                for index, selected_tag in enumerate(self.selected_tags)
                if self._normalized_tag_name(selected_tag) == tag_name
            ),
            None,
        )
        if matching_selected_index is None:
            self.selected_tags.append(clean_tag)
        else:
            self.selected_tags[matching_selected_index] = clean_tag

        self.search_value.set("")
        self._render_selected_tags()
        self._render_preset_tags()
        self._schedule_reposition()

    def _build_selector(self):
        ctk.CTkLabel(
            self,
            text="Tags",
            font=self.fonts["body_bold"],
            text_color=colors.TEXT_PRIMARY,
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            self,
            text="Optional",
            font=self.fonts["small"],
            text_color=colors.TEXT_SECONDARY,
        ).grid(row=0, column=1, sticky="e")

        self.search_entry = ctk.CTkEntry(
            self,
            textvariable=self.search_value,
            placeholder_text="🔍  Search preset tags, or create new ones!",
            font=self.fonts["body"],
            text_color=colors.TEXT_PRIMARY,
            placeholder_text_color=colors.TEXT_SECONDARY,
            fg_color=colors.SURFACE_HOVER,
            border_color=colors.BORDER,
            corner_radius=spacing.RADIUS_MEDIUM,
            height=38,
        )
        self.search_entry.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(spacing.SPACE_2, 0),
        )

        self.selected_tags_frame = ctk.CTkFrame(
            self,
            fg_color=colors.TRANSPARENT,
        )
        self.selected_tags_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(spacing.SPACE_2, 0),
        )

    def _build_dropdown(self):
        self.dropdown = ctk.CTkFrame(
            self.overlay_parent,
            width=100,
            height=self.DROPDOWN_HEIGHT,
            fg_color=colors.SURFACE,
            border_width=1,
            border_color=colors.BORDER,
            corner_radius=spacing.RADIUS_MEDIUM,
        )
        self.dropdown.grid_columnconfigure(0, weight=1)
        self.dropdown.grid_rowconfigure(0, weight=1)
        self.dropdown.grid_propagate(False)

        self.preset_list = ctk.CTkScrollableFrame(
            self.dropdown,
            fg_color=colors.SURFACE,
            corner_radius=0,
        )
        self.preset_list.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=spacing.SPACE_1,
            pady=(spacing.SPACE_1, 0),
        )
        self.preset_list.grid_columnconfigure(0, weight=1)

        self.create_button = ctk.CTkButton(
            self.dropdown,
            text="+ Create new tag",
            font=self.fonts["body"],
            text_color=colors.TEXT_SECONDARY,
            fg_color=colors.SURFACE,
            hover_color=colors.SURFACE_HOVER,
            border_width=1,
            border_color=colors.BORDER,
            corner_radius=spacing.RADIUS_MEDIUM,
            height=34,
            cursor="hand2",
            command=self._create_tag,
        )
        self.create_button.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=spacing.SPACE_2,
            pady=spacing.SPACE_2,
        )

    def _filter_tags(self, *_args):
        self._render_preset_tags()

    def _render_preset_tags(self):
        for widget in self.preset_list.winfo_children():
            widget.destroy()

        query = self.search_value.get().strip().casefold()
        selected_names = {
            self._normalized_tag_name(tag)
            for tag in self.selected_tags
        }

        visible_tags = [
            tag
            for tag in self.available_tags
            if self._normalized_tag_name(tag) not in selected_names
            and query in self._normalized_tag_name(tag)
        ]

        for row, tag in enumerate(visible_tags):
            tag_button = ctk.CTkButton(
                self.preset_list,
                text=tag["tag_name"],
                font=self.fonts["body"],
                text_color=tag["color_hex"],
                fg_color=colors.SURFACE,
                hover_color=colors.SURFACE_HOVER,
                border_width=1,
                border_color=tag["color_hex"],
                corner_radius=spacing.RADIUS_MEDIUM,
                height=30,
                cursor="hand2",
                command=lambda value=tag: self._select_tag(value),
            )
            tag_button.grid(
                row=row,
                column=0,
                sticky="ew",
                padx=spacing.SPACE_1,
                pady=(spacing.SPACE_1, 0),
            )


    def _render_selected_tags(self):
        for widget in self.selected_tags_frame.winfo_children():
            widget.destroy()

        if not self.selected_tags:
            self.selected_tags_frame.grid_remove()
            return

        self.selected_tags_frame.grid()
        for tag in self.selected_tags:
            chip = ctk.CTkButton(
                self.selected_tags_frame,
                text=f"{tag['tag_name']}  ×",
                font=self.fonts["body"],
                text_color=tag["color_hex"],
                fg_color=colors.SURFACE,
                hover_color=colors.SURFACE_HOVER,
                border_width=1,
                border_color=tag["color_hex"],
                corner_radius=spacing.RADIUS_MEDIUM,
                height=30,
                cursor="hand2",
                command=lambda value=tag: self._remove_tag(value),
            )
            chip.pack(
                side="left",
                padx=(0, spacing.SPACE_1),
            )

    def _select_tag(self, tag):
        tag_name = self._normalized_tag_name(tag)
        if not any(
            self._normalized_tag_name(selected_tag) == tag_name
            for selected_tag in self.selected_tags
        ):
            self.selected_tags.append(tag)

        self.search_value.set("")
        self._render_selected_tags()
        self._render_preset_tags()
        self._schedule_reposition()

    def _remove_tag(self, tag):
        self.selected_tags.remove(tag)
        self._render_selected_tags()
        self._render_preset_tags()
        self._schedule_reposition()

    def _show_dropdown(self, _event=None):
        self._dropdown_visible = True
        self._render_preset_tags()
        self._schedule_reposition()

    def _schedule_reposition(self, _event=None):
        try:
            selector_exists = self.winfo_exists()
        except TclError:
            return

        if not self._dropdown_visible or not selector_exists:
            return

        if self._reposition_job is not None:
            self.after_cancel(self._reposition_job)

        self._reposition_job = self.after_idle(self._position_dropdown)

    def _position_dropdown(self):
        self._reposition_job = None
        try:
            selector_exists = self.winfo_exists()
            entry_is_mapped = self.search_entry.winfo_ismapped()
        except TclError:
            return

        if not self._dropdown_visible or not selector_exists:
            return
        if not entry_is_mapped:
            self._hide_dropdown()
            return

        self.overlay_parent.update_idletasks()
        entry_width = self.search_entry.winfo_width()
        entry_x = (
            self.search_entry.winfo_rootx()
            - self.overlay_parent.winfo_rootx()
        )
        entry_top = (
            self.search_entry.winfo_rooty()
            - self.overlay_parent.winfo_rooty()
        )
        entry_height = self.search_entry.winfo_height()
        overlay_height = self.overlay_parent.winfo_height()

        if entry_top + entry_height <= 0 or entry_top >= overlay_height:
            self._hide_dropdown()
            return

        gap = self.dropdown._apply_widget_scaling(spacing.SPACE_1)
        requested_height = self.dropdown._apply_widget_scaling(
            self.DROPDOWN_HEIGHT
        )
        _side, dropdown_y, dropdown_height = calculate_dropdown_geometry(
            entry_top,
            entry_height,
            overlay_height,
            requested_height,
            gap,
        )

        if dropdown_height <= 0:
            self._hide_dropdown()
            return

        to_logical_units = self.dropdown._reverse_widget_scaling

        self.dropdown.configure(
            width=to_logical_units(float(entry_width)),
            height=to_logical_units(float(dropdown_height)),
        )
        self.dropdown.place(
            x=to_logical_units(float(entry_x)),
            y=to_logical_units(float(dropdown_y)),
        )
        self.dropdown.lift()

    def _bind_overlay_events(self):
        toplevel = self.winfo_toplevel()
        bindings = (
            (toplevel, "<Button-1>", self._close_on_outside_click),
            (toplevel, "<Configure>", self._handle_toplevel_configure),
            (toplevel, "<MouseWheel>", self._schedule_reposition),
            (toplevel, "<Button-4>", self._schedule_reposition),
            (toplevel, "<Button-5>", self._schedule_reposition),
            (toplevel, "<B1-Motion>", self._schedule_reposition),
            (toplevel, "<ButtonRelease-1>", self._schedule_reposition),
            (toplevel, "<KeyRelease>", self._schedule_reposition),
        )

        for widget, sequence, callback in bindings:
            binding_id = widget.bind(sequence, callback, add=True)
            self._binding_ids.append((widget, sequence, binding_id))

    def _handle_toplevel_configure(self, event):
        try:
            toplevel = self.winfo_toplevel()
        except TclError:
            return

        if event.widget is toplevel:
            self._schedule_reposition()

    def _close_on_outside_click(self, event):
        if self._is_inside(event.widget, self.search_entry):
            return
        if self._is_inside(event.widget, self.dropdown):
            return
        self._hide_dropdown()

    def _hide_dropdown(self):
        self._dropdown_visible = False
        if self._reposition_job is not None:
            try:
                self.after_cancel(self._reposition_job)
            except TclError:
                pass
            self._reposition_job = None
        self.dropdown.place_forget()

    def _cleanup_bindings(self, _event=None):
        if self._cleanup_complete:
            return
        self._cleanup_complete = True
        self._dropdown_visible = False

        if self._reposition_job is not None:
            try:
                self.after_cancel(self._reposition_job)
            except TclError:
                pass
            self._reposition_job = None

        for widget, sequence, binding_id in self._binding_ids:
            try:
                widget.unbind(sequence, binding_id)
            except TclError:
                pass
        self._binding_ids.clear()

        try:
            if self.dropdown.winfo_exists():
                self.dropdown.place_forget()
                self.dropdown.destroy()
        except TclError:
            pass

    @staticmethod
    def _is_inside(widget, container):
        while widget is not None:
            if widget == container:
                return True
            widget = getattr(widget, "master", None)
        return False

    def _create_tag(self):
        self._hide_dropdown()
        if self.on_create_tag is not None:
            self.on_create_tag()
