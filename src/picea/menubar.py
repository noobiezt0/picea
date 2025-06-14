from customtkinter import CTkButton, CTkFrame
from customtkinter.windows.widgets.core_widget_classes import DropdownMenu

class MenuCascade(CTkButton):
    def __init__(self, master=None, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self._dropdown_menu = DropdownMenu(self, values=list())
        self.configure(command=self._open_dropdown_menu)

    def _open_dropdown_menu(self) -> None:
        self._dropdown_menu.open(
            self.winfo_rootx(),
            self.winfo_rooty() + self._apply_widget_scaling(self._current_height)
        )

    def add_command(self, *args, **kwargs) -> None:
        self._dropdown_menu.add_command(*args, **kwargs)

    def add_separator(self, *args, **kwargs) -> None:
        self._dropdown_menu.add_separator(*args, **kwargs)

class Menubar(CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.menu = dict()
        self.window = None

    def add_cascade(self, name: str, **kwargs) -> None:
        self.menu[name] = MenuCascade(
            self,
            width=0,
            text=name,
            corner_radius=0,
            fg_color="transparent",
            hover_color=('#f0f0f0', '#121212'),
            **kwargs
        )

    def pack_cascades(self, *args, **kwargs) -> None:
        for cascade in self.menu:
            self.menu[cascade].pack(*args, **kwargs)

    def add_command(self, cascade: str, **kwargs) -> None:
        self.menu[cascade].add_command(**kwargs)

    def add_separator(self, cascade: str, **kwargs) -> None:
        self.menu[cascade].add_separator(**kwargs)
