from gui_widgets.tag_selector import calculate_dropdown_geometry


def test_dropdown_opens_below_when_requested_height_fits():
    side, dropdown_y, dropdown_height = calculate_dropdown_geometry(
        entry_top=100,
        entry_height=40,
        overlay_height=600,
        requested_height=210,
        gap=4,
    )

    assert side == "below"
    assert dropdown_y == 144
    assert dropdown_height == 210


def test_dropdown_opens_above_when_below_does_not_fit():
    side, dropdown_y, dropdown_height = calculate_dropdown_geometry(
        entry_top=500,
        entry_height=40,
        overlay_height=600,
        requested_height=210,
        gap=4,
    )

    assert side == "above"
    assert dropdown_y == 286
    assert dropdown_height == 210


def test_dropdown_constrains_height_to_larger_available_side():
    side, dropdown_y, dropdown_height = calculate_dropdown_geometry(
        entry_top=130,
        entry_height=40,
        overlay_height=300,
        requested_height=210,
        gap=4,
    )

    assert side == "below"
    assert dropdown_y == 174
    assert dropdown_height == 126
