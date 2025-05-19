"""

abies, part of the Picea Notepad project.

abies is a simple layout builder for CustomTkinter,
using JSON files you can make layouts with ease.

"""

import customtkinter as ctk
from PIL import Image

from typing import TextIO
import json

class abies:
    def __init__(
        self,
        master: ctk.CTk | ctk.CTkFrame | ctk.CTkToplevel
    ) -> None:
        self._master = master
        self._layout = dict()
        self.widgets = dict()

    def load(self, layout: TextIO | str) -> None:
        if isinstance(layout, str):
            self._layout = json.loads(layout)
        else:
            self._layout = json.load(layout)

        for widget in self._layout:
            temp = getattr(ctk, 'CTk' + widget.split('-', maxsplit=1)[0])

            if 'font' in self._layout[widget]:
                font = self._layout[widget]['font']
                self._layout[widget]['font'] = ctk.CTkFont(**font)

            if 'image' in self._layout[widget]:
                image = self._layout[widget]['image']

                if 'light_image' in image:
                    light_image = image['light_image']
                    image['light_image'] = Image.open(**light_image)
                if 'dark_image' in image:
                    dark_image = image['dark_image']
                    image['dark_image'] = Image.open(**dark_image)

                self._layout[widget]['image'] = ctk.CTkImage(**image)

            if 'pack' in self._layout[widget]:
                pack = self._layout[widget].pop('pack', None)
                self.widgets[widget] = temp(self._master, **self._layout[widget])
                self.widgets[widget].pack(**pack)

_demo = """
{
  "Label": {
    "pack": {
      "anchor": "center",
      "expand": true
    }
  },
  "Label.": {
    "pack": {
      "anchor": "center",
      "expand": true
    }
  }
}
"""

if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry('240x120')
    abies(app).load(_demo)
    app.mainloop()
