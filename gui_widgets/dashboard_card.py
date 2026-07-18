import customtkinter as ctk
from gui_style import colors, spacing

class DashboardCard(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        fonts,
        title,
        description,
        accent_color,
        command=None,
    ):
        super().__init__(
            parent,
            fg_color=colors.SURFACE,
            corner_radius=spacing.RADIUS_LARGE,
            border_width=spacing.CARD_BORDER_WIDTH,
            border_color=colors.BORDER,
        )

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=fonts["subtitle"],
            text_color=colors.TEXT_PRIMARY,
            fg_color=colors.TRANSPARENT,
        )

        self.description_label = ctk.CTkLabel(
            self,
            text=description,
            font=fonts["body"],
            text_color=colors.TEXT_SECONDARY,
            fg_color=colors.TRANSPARENT,
            wraplength=spacing.CARD_MIN_WIDTH - 2 * spacing.CARD_PADDING,
            justify="left",
        )

        self.accent_frame = ctk.CTkFrame(
            self,
            width=spacing.CARD_ACCENT_WIDTH,
            fg_color=accent_color,
            corner_radius=spacing.RADIUS_LARGE,
        )

        self.title_label.grid(
            row=0,
            column=1,
            padx=(spacing.CARD_PADDING, spacing.CARD_PADDING),
            pady=(spacing.CARD_PADDING, 0),
            sticky="nw",
        )
        self.description_label.grid(
            row=1,
            column=1,
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

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_hover_enter)
        self.bind("<Leave>", self._on_hover_leave)

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
