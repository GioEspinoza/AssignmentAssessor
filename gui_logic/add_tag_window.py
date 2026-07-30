import customtkinter as ctk
from CTkColorPicker import AskColor


def add_tag_popup(parent, fonts, on_tag_added):
    popup = ctk.CTkToplevel(parent)
    popup.title("Add Tag")
    popup.geometry("400x250")
    popup.resizable(False, False)
    popup.transient(parent.winfo_toplevel())

    selected_color = "#3B82F6"

    def choose_color():
        nonlocal selected_color
        picker = AskColor(
            title="Choose Tag Color",
            initial_color=selected_color,
            text="Use Color",
        )
        picker.transient(popup)

        try:
            color = picker.get()
        finally:
            if popup.winfo_exists():
                popup.grab_set()

        if color:
            selected_color = color
            color_button.configure(
                text=color,
                fg_color=color,
                hover_color=color,
                border_color=color,
            )

    def add_tag():
        tag_name = tag_entry.get().strip()
        if not tag_name:
            return

        on_tag_added(
            {
                "tag_name": tag_name,
                "color_hex": selected_color,
            }
        )
        popup.destroy()

    content_frame = ctk.CTkFrame(
        popup,
        fg_color="transparent",
    )
    content_frame.pack(
        expand=True,
        fill="both",
        padx=20,
        pady=20,
    )

    ctk.CTkLabel(
        content_frame,
        text="Tag Name:",
        font=fonts["body"],
    ).pack(
        anchor="w",
        pady=(0, 5),
    )
    tag_entry = ctk.CTkEntry(
        content_frame,
        font=fonts["body"],
    )
    tag_entry.pack(
        fill="x",
        pady=(0, 10),
    )

    color_button = ctk.CTkButton(
        content_frame,
        text="Choose Color",
        font=fonts["body"],
        command=choose_color,
    )
    color_button.pack(pady=(0, 10))

    add_button = ctk.CTkButton(
        content_frame,
        text="Add Tag",
        font=fonts["body"],
        command=add_tag,
    )
    add_button.pack(pady=(10, 0))

    popup.wait_visibility()
    popup.grab_set()
    tag_entry.focus_set()
