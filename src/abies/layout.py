import customtkinter as ctk

from typing import TextIO
import json

class Layout:
    def __init__(
        self,
        master: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame
    ) -> None:
        self._master = master
        self._layout = dict()
        self.widgets = dict()

    def load(self, layout: TextIO) -> None:
        if isinstance(layout, str):
            self._layout = json.loads(layout)
        else:
            self._layout = json.load(layout)

        for widget in self._layout:
            temp = getattr(ctk, 'CTk' + widget.split('-', maxsplit=1)[0])

            if 'font' in self._layout[widget]:
                font = self._layout[widget]['font']
                self._layout[widget]['font'] = ctk.CTkFont(**font)

            if 'pack' in self._layout[widget]:
                pack = self._layout[widget].pop('pack', None)
                self.widgets[widget] = temp(self._master, **self._layout[widget])
                self.widgets[widget].pack(**pack)
