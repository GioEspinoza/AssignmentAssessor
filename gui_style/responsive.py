import customtkinter as ctk


def clone_fonts(fonts):
    return {
        name: ctk.CTkFont(
            family=font.cget("family"),
            size=font.cget("size"),
            weight=font.cget("weight"),
        )
        for name, font in fonts.items()
    }


class ResponsiveText:
    def __init__(
        self,
        parent,
        fonts,
        base_width=900,
        min_scale=0.85,
        max_scale=1.25,
    ):
        self.fonts = fonts
        self.base_width = base_width
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.base_sizes = {
            name: font.cget("size")
            for name, font in fonts.items()
        }
        self.current_sizes = {}

        parent.bind("<Configure>", self._resize_text, add="+")

    def _resize_text(self, event):
        scale = max(
            self.min_scale,
            min(event.width / self.base_width, self.max_scale),
        )

        for name, font in self.fonts.items():
            new_size = round(self.base_sizes[name] * scale)

            if self.current_sizes.get(name) != new_size:
                font.configure(size=new_size)
                self.current_sizes[name] = new_size
