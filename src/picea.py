from customtkinter import CTkFrame, CTkButton, CTkTextbox, CTkScrollbar
from customtkinter.windows.widgets.core_widget_classes import DropdownMenu

class WelcomePage(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._widgets = list()

    def add(self, widget):
        self._widgets.append(widget)

    def cfg_buttons(self, **kwargs):
        for widget in self._widgets:
            if isinstance(widget, CTkButton):
                widget.configure(**kwargs)

    def pack_all(self, **kwargs):
        for widget in self._widgets:
            widget.pack(**kwargs)

class Textbox(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textbox = CTkTextbox(self, activate_scrollbars=False)
        self.scrollbar = CTkScrollbar(self, command=self.textbox.yview, width=6)
        self.textbox.configure(yscrollcommand=self.scrollbar.set)
        self.linenums = CTkTextbox(self, activate_scrollbars=False, width=64, text_color='#969696')

        self.statusbar = Menubar(self, height=16, fg_color="transparent")
        self.statusbar.pack(side='bottom', fill='x', padx=3, pady=(0, 3))
        self.statusbar.add_cascade('Encoding')
        self.statusbar.add_cascade('CRLF')
        self.statusbar.add_cascade('1:0')
        self.statusbar.pack_cascades(side='right', ipadx=8)

        self.scrollbar.pack(side='right', fill='y', padx=3, pady=(0, 3))
        self.textbox.pack(side='right', fill='both', pady=(0, 3), expand=True)
        self.linenums.pack(side='left', fill='y', padx=3, pady=(0, 3))


class CTkDropdownMenu(DropdownMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MenuCascade(CTkButton):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._dropdown_menu = CTkDropdownMenu(self, values=list())
        self.configure(command=self._open_dropdown_menu)

    def _open_dropdown_menu(self):
        self._dropdown_menu.open(
            self.winfo_rootx(),
            self.winfo_rooty() + self._apply_widget_scaling(self._current_height)
        )

    def add_command(self, *args, **kwargs):
        self._dropdown_menu.add_command(*args, **kwargs)

    def add_separator(self, *args, **kwargs):
        self._dropdown_menu.add_separator(*args, **kwargs)

class Menubar(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = dict()
        self.window = None

    def add_cascade(self, name: str, **kwargs):
        self.menu[name] = MenuCascade(
            self,
            width=0,
            text=name,
            corner_radius=0,
            fg_color="transparent",
            hover_color=('#f0f0f0', '#121212'),
            **kwargs
        )

    def pack_cascades(self, *args, **kwargs):
        for cascade in self.menu:
            self.menu[cascade].pack(*args, **kwargs)

    def add_command(self, cascade: str, **kwargs):
        self.menu[cascade].add_command(**kwargs)

    def add_separator(self, cascade: str, **kwargs):
        self.menu[cascade].add_separator(**kwargs)
