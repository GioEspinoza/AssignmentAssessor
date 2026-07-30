import customtkinter as ctk

from gui_style import colors, spacing
from gui_widgets.widgets import enable_linux_mousewheel


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
        self.available_tags = available_tags
        self.selected_tags = []
        self.on_create_tag = on_create_tag

        self.search_value = ctk.StringVar()
        self.search_value.trace_add("write", self._filter_tags)

        self.grid_columnconfigure(0, weight=1)
        self._build_selector()
        self._build_dropdown()
        self._render_selected_tags()
        self._render_preset_tags()

        self.search_entry.bind("<Button-1>", self._show_dropdown, add=True)
        self.search_entry.bind("<FocusIn>", self._show_dropdown)
        self.winfo_toplevel().bind(
            "<Button-1>",
            self._close_on_outside_click,
            add=True,
        )

    def get_selected_tags(self):
        return list(self.selected_tags)

    def add_tag(self, tag):
        self.available_tags.append(tag)
        self._select_tag(tag)

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
            fg_color=colors.TRANSPARENT,
            border_width=1,
            border_color=colors.BORDER,
            corner_radius=spacing.RADIUS_MEDIUM,
        )
        self.dropdown.grid_columnconfigure(0, weight=1)
        self.dropdown.grid_rowconfigure(0, weight=1)
        self.dropdown.grid_propagate(False)

        self.preset_list = ctk.CTkScrollableFrame(
            self.dropdown,
            fg_color=colors.TRANSPARENT,
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

        create_button = ctk.CTkButton(
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
        create_button.grid(
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
        selected_names = {tag["tag_name"].casefold() for tag in self.selected_tags}

        visible_tags = [
            tag
            for tag in self.available_tags
            if tag["tag_name"].casefold() not in selected_names
            and query in tag["tag_name"].casefold()
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

        enable_linux_mousewheel(self.preset_list)

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
        self.selected_tags.append(tag)
        self.search_value.set("")
        self._render_selected_tags()
        self._render_preset_tags()

    def _remove_tag(self, tag):
        self.selected_tags.remove(tag)
        self._render_selected_tags()
        self._render_preset_tags()

    def _show_dropdown(self, _event=None):
        self.overlay_parent.update_idletasks()
        self.dropdown.configure(width=self.search_entry.winfo_width())
        self.dropdown.place(
            x=(self.search_entry.winfo_rootx() - self.overlay_parent.winfo_rootx()),
            y=(
                self.search_entry.winfo_rooty()
                - self.overlay_parent.winfo_rooty()
                + self.search_entry.winfo_height()
                + spacing.SPACE_1
            ),
        )
        self.dropdown.lift()

    def _close_on_outside_click(self, event):
        if self._is_inside(event.widget, self.search_entry):
            return
        if self._is_inside(event.widget, self.dropdown):
            return
        self.dropdown.place_forget()

    @staticmethod
    def _is_inside(widget, container):
        while widget is not None:
            if widget == container:
                return True
            widget = getattr(widget, "master", None)
        return False

    def _create_tag(self):
        self.dropdown.place_forget()
        if self.on_create_tag is not None:
            self.on_create_tag()
