"""Shared spacing and sizing tokens for UI layout."""

SPACE_1 = 4
SPACE_2 = 8
SPACE_3 = 12
SPACE_4 = 16
SPACE_5 = 20
SPACE_6 = 24
SPACE_8 = 32
SPACE_10 = 40
SPACE_12 = 48

PAGE_X = SPACE_8
PAGE_Y = SPACE_5
SECTION_GAP = SPACE_6
GRID_GAP = SPACE_4
CARD_PADDING = SPACE_5

RADIUS_SMALL = 8
RADIUS_MEDIUM = 12
RADIUS_LARGE = 16

__all__ = [name for name in globals() if name.isupper()]
