import sys


def enable_linux_mousewheel(scrollable_frame, units=1):
    """Add Linux/X11 wheel events to a CustomTkinter scrollable frame."""
    if not sys.platform.startswith("linux"):
        return

    canvas = getattr(scrollable_frame, "_parent_canvas", None)
    if canvas is None:
        return

    def scroll(event, direction):
        if canvas.yview() != (0.0, 1.0):
            canvas.yview_scroll(direction * units, "units")
        return "break"

    def bind_widget_tree(widget):
        try:
            widget.bind(
                "<Button-4>",
                lambda event: scroll(event, -1),
                add="+",
            )
            widget.bind(
                "<Button-5>",
                lambda event: scroll(event, 1),
                add="+",
            )
        except NotImplementedError:
            # Some composite CustomTkinter widgets, such as
            # CTkSegmentedButton, intentionally disable direct bindings.
            pass

        for child in widget.winfo_children():
            bind_widget_tree(child)

    bind_widget_tree(scrollable_frame)
    canvas.bind(
        "<Button-4>",
        lambda event: scroll(event, -1),
        add="+",
    )
    canvas.bind(
        "<Button-5>",
        lambda event: scroll(event, 1),
        add="+",
    )


__all__ = ["enable_linux_mousewheel"]
