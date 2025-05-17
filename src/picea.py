from customtkinter import CTkFrame, CTkButton, CTkTextbox, CTkScrollbar, CTkLabel
from customtkinter.windows.widgets.core_widget_classes import DropdownMenu

class Textbox(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textbox = CTkTextbox(self, activate_scrollbars=False)
        self.scrollbar = CTkScrollbar(self, command=self.textbox.yview, width=6)
        self.textbox.configure(yscrollcommand=self.scrollbar.set)
        self.linenums = CTkTextbox(self, activate_scrollbars=False, width=64, text_color='#969696')

        self.scrollbar.pack(side='right', fill='y', padx=3, pady=(0, 3))
        self.textbox.pack(side='right', fill='both', pady=(0, 3), expand=True)
        self.linenums.pack(side='left', fill='y', padx=3, pady=(0, 3))


class CTkDropdownMenu(DropdownMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_menu_commands()
        self._add_separators()
    def _add_separators(self):
        for value in self._values:
            if value == '***':
                index = self._values.index('***')
                self.delete(index, index)
                self.insert(index, itemType='separator')

class MenuCascade(CTkButton):
    def __init__(self, master=None, values: list | None = None, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        self._values = values
        self._dropdown_menu = CTkDropdownMenu(
            master=self, values=self._values
        )
        self.configure(command=self._open_dropdown_menu)

    def _open_dropdown_menu(self):
        self._dropdown_menu.open(
            self.winfo_rootx(),
            self.winfo_rooty() + self._apply_widget_scaling(self._current_height)
        )

class Menubar(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = dict()
        self.window = None

    def add_cascade(self, name: str, values: list):
        self.menu[name] = MenuCascade(
            self,
            width=0,
            text=name,
            values=values,
            corner_radius=0,
            fg_color=('white', '#000000'),
            hover_color=('f0f0f0', '#121212')
        )
        self.menu[name].pack(side='left', anchor='nw', ipadx=8)
