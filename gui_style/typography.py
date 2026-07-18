from tkinter import font as tkfont
import customtkinter as ctk

_fonts_cache: dict[str, ctk.CTkFont] | None = None

__all__ = ["create_fonts"]


def create_fonts(root: ctk.CTk) -> dict[str, ctk.CTkFont]:

    global _fonts_cache

    if _fonts_cache is not None:
        return _fonts_cache

    available_families = {
        family.casefold(): family
        for family in tkfont.families(root=root)
    }

    def select_family(*candidates: str) -> str:
        for candidate in candidates:
            installed_name = available_families.get(candidate.casefold())

            if installed_name is not None:
                return installed_name

        return candidates[-1]

    ui_family = select_family(
        "Inter",
        "Segoe UI",
        "Arial",
        "DejaVu Sans",
    )

    brand_family = select_family(
        "Inter Display",
        "Inter",
        "Segoe UI",
        "Arial",
        "DejaVu Sans",
    )

    monospace_family = select_family(
        "JetBrains Mono",
        "Consolas",
        "DejaVu Sans Mono",
    )

    body_font = ctk.CTkFont(
        family=ui_family,
        size=14,
    )

    body_bold_font = ctk.CTkFont(
        family=ui_family,
        size=14,
        weight="bold",
    )

    _fonts_cache = {
        "brand": ctk.CTkFont(
            family=brand_family,
            size=48,
            weight="bold",
        ),
        "display": ctk.CTkFont(
            family=ui_family,
            size=40,
            weight="bold",
        ),
        "page_title": ctk.CTkFont(
            family=ui_family,
            size=28,
            weight="bold",
        ),
        "section_title": ctk.CTkFont(
            family=ui_family,
            size=20,
            weight="bold",
        ),
        "card_title": ctk.CTkFont(
            family=ui_family,
            size=17,
            weight="bold",
        ),
        "subtitle": ctk.CTkFont(
            family=ui_family,
            size=16,
        ),
        "body": body_font,
        "body_bold": body_bold_font,
        "small": ctk.CTkFont(
            family=ui_family,
            size=12,
        ),
        "small_bold": ctk.CTkFont(
            family=ui_family,
            size=12,
            weight="bold",
        ),
        "button": body_bold_font,
        "input": body_font,
        "stat": ctk.CTkFont(
            family=ui_family,
            size=24,
            weight="bold",
        ),
        "timer": ctk.CTkFont(
            family=ui_family,
            size=48,
            weight="bold",
        ),
        "monospace": ctk.CTkFont(
            family=monospace_family,
            size=13,
        ),
    }

    return _fonts_cache
