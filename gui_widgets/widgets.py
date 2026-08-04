import customtkinter as ctk

from gui_style import colors


HEADER_ACTION_HEIGHT = 32
HEADER_ACTION_HORIZONTAL_PADDING = 14


def create_header_action(parent, *, text, font, command):
    text_width = max(0, int(font.measure(text)))

    return ctk.CTkButton(
        parent,
        text=text,
        font=font,
        width=text_width + (HEADER_ACTION_HORIZONTAL_PADDING * 2),
        height=HEADER_ACTION_HEIGHT,
        corner_radius=HEADER_ACTION_HEIGHT // 2,
        fg_color=colors.ACCENT,
        hover_color=colors.ACCENT_HOVER,
        text_color=colors.TEXT_ON_ACCENT,
        cursor="hand2",
        command=command,
    )
__all__ = ["create_header_action"]
