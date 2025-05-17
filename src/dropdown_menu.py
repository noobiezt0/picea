from customtkinter.windows.widgets.core_widget_classes import DropdownMenu

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
