import customtkinter as ctk
from gui_style import colors, spacing
from gui_style.responsive import ResponsiveText

class DashboardCard(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        fonts,
        title,
        description,
        accent_color,
        icon,
        command=None,
    ):
        super().__init__(
            parent,
            fg_color=colors.SURFACE,
            corner_radius=spacing.RADIUS_LARGE,
            border_width=spacing.CARD_BORDER_WIDTH,
            border_color=colors.BORDER,
        )

        font_family = fonts["body"].cget("family")
        self.card_fonts = {
            "title": ctk.CTkFont(
                family=font_family,
                size=18,
                weight="bold",
            ),
            "body": ctk.CTkFont(
                family=font_family,
                size=15,
            ),
            "icon": ctk.CTkFont(
                family=font_family,
                size=26,
                weight="bold",
            ),
        }

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=self.card_fonts["title"],
            text_color=colors.TEXT_PRIMARY,
            fg_color=colors.TRANSPARENT,
        )

        self.description_label = ctk.CTkLabel(
            self,
            text=description,
            font=self.card_fonts["body"],
            text_color=colors.TEXT_SECONDARY,
            fg_color=colors.TRANSPARENT,
            wraplength=spacing.CARD_MIN_WIDTH - 2 * spacing.CARD_PADDING,
            justify="left",
        )

        self.icon_label = ctk.CTkLabel(
            self,
            text=icon,
            font=self.card_fonts["icon"],
            text_color=accent_color,
            fg_color=colors.TRANSPARENT,
        )

        self.accent_frame = ctk.CTkFrame(
            self,
            width=spacing.CARD_ACCENT_WIDTH,
            fg_color=accent_color,
            corner_radius=spacing.RADIUS_LARGE,
        )

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label.grid(
            row=0,
            column=1,
            padx=(spacing.CARD_PADDING, spacing.SPACE_2),
            pady=(spacing.CARD_PADDING, 0),
            sticky="nw",
        )
        self.icon_label.grid(
            row=0,
            column=2,
            padx=(spacing.SPACE_2, spacing.CARD_PADDING),
            pady=(spacing.SPACE_2, 0),
            sticky="ne",
        )
        self.description_label.grid(
            row=1,
            column=1,
            columnspan=2,
            padx=(spacing.CARD_PADDING, spacing.CARD_PADDING),
            pady=(spacing.SPACE_2, spacing.CARD_PADDING),
            sticky="nw",
        )
        self.accent_frame.grid(
            row=0,
            column=0,
            rowspan=2,
            sticky="nsw",
        )

        self.command = command

        for widget in (
            self,
            self.title_label,
            self.description_label,
            self.icon_label,
            self.accent_frame,
        ):
            widget.bind("<Button-1>", self._on_click)
            widget.bind("<Enter>", self._on_hover_enter)
            widget.bind("<Leave>", self._on_hover_leave)

        self.bind("<Configure>", self._resize_description)
        self.responsive_text = ResponsiveText(
            self,
            self.card_fonts,
            base_width=300,
            min_scale=0.9,
            max_scale=1.25,
        )

    def _resize_description(self, event):
        card_width = event.width

        self.description_label.configure(
            wraplength=max(
                140,
                card_width - spacing.CARD_ACCENT_WIDTH - 2 * spacing.CARD_PADDING - spacing.SPACE_2,
            )
        )

    def _on_hover_enter(self, event):
        self.configure(fg_color=colors.SURFACE_HOVER)

        if self.command:
            self.configure(cursor="hand2")

    def _on_hover_leave(self, event):
        self.configure(fg_color=colors.SURFACE)

        if self.command:
            self.configure(cursor="")

    def _on_click(self, event):
        if self.command:
            self.command()
