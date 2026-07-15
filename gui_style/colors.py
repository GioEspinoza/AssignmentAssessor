"""Shared color tokens for the Assignment Assessor UI."""

Color = str | tuple[str, str]

TRANSPARENT: Color = "transparent"

APP_BACKGROUND: Color = ("#F5F7FB", "#111827")
SURFACE: Color = ("#FFFFFF", "#1F2937")
SURFACE_HOVER: Color = ("#F1F5F9", "#273449")
BORDER: Color = ("#D7DEE8", "#374151")
DIVIDER: Color = ("#CBD5E1", "#374151")

TEXT_PRIMARY: Color = ("#111827", "#F9FAFB")
TEXT_SECONDARY: Color = ("#64748B", "#9CA3AF")
TEXT_ON_ACCENT: Color = "#FFFFFF"

ACCENT: Color = ("#2563EB", "#3B82F6")
ACCENT_HOVER: Color = ("#1D4ED8", "#2563EB")
SUCCESS: Color = ("#15803D", "#22C55E")
WARNING: Color = ("#B45309", "#F59E0B")
DANGER: Color = ("#DC2626", "#EF4444")

# Dashboard card accents
ASSIGNMENTS_ACCENT: Color = ("#2563EB", "#3B82F6")
URGENT_ACCENT: Color = ("#DC2626", "#EF4444")
CALENDAR_ACCENT: Color = ("#7C3AED", "#8B5CF6")
PLANNER_ACCENT: Color = ("#059669", "#10B981")
ANALYTICS_ACCENT: Color = ("#D97706", "#F59E0B")
LOCK_IN_ACCENT: Color = ("#DB2777", "#EC4899")

__all__ = [name for name in globals() if name.isupper()]
