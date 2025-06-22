from customtkinter import CTkFrame, CTkTextbox, CTkScrollbar
from picea.menubar import Menubar

from typing import TextIO

class TextboxFrame(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textbox = CTkTextbox(self, wrap='none', activate_scrollbars=False, undo=True)

        self._vscrollbar = CTkScrollbar(self, command=self.textbox.yview, width=6)
        self._hscrollbar = CTkScrollbar(self, command=self.textbox.xview, orientation='horizontal', height=6)
        self.textbox.configure(yscrollcommand=self._vscrollbar.set, xscrollcommand=self._hscrollbar.set)

        self.linenums = CTkTextbox(
            self,
            state='disabled',
            activate_scrollbars=False,
            width=60,
            text_color='#969696',
            wrap='none',
        )
        self.linenums.tag_config('right', justify='right')

        self.statusbar = Menubar(self, height=16, fg_color='transparent')
        self.statusbar.pack(side='bottom', fill='x', padx=3, pady=(0, 3))
        self.statusbar.add_cascade('Encoding')
        self.statusbar.add_cascade('Line Ending')
        self.statusbar.add_cascade('Position')
        self.statusbar.pack_cascades(side='right', ipadx=8)

        self._vscrollbar.pack(side='right', fill='y', padx=3, pady=(0, 16))
        self._hscrollbar.pack(side='bottom', fill='x', padx=3, pady=(0, 6))
        self.textbox.pack(side='right', fill='both', pady=(0, 3), expand=True)
        self.linenums.pack(side='left', fill='y', padx=3, pady=(0, 3))

        self.textbox.bind('<<Modified>>', self._update_linenums)
        self.textbox.bind('<MouseWheel>', self._update_linenums)
        self.textbox.bind('<<Cut>>', self._update_linenums)
        self.textbox.bind('<<Copy>>', self._update_linenums)
        self.textbox.bind('<<Paste>>', self._update_linenums)
        self.textbox.bind('<Button-4>', self._update_linenums)
        self.textbox.bind('<Button-5>', self._update_linenums)
        self.textbox.bind('<KeyRelease>', self._update_position)
        self.textbox.bind('<Button-1>', self._update_position)

        self._update_linenums()
        self._update_position()

    def _update_linenums(self, event=None):
        self.textbox.edit_modified(False)

        lines = self.textbox.get('1.0', 'end-1c').count('\n') + 1
        linenums = '\n'.join(str(i) for i in range(1, lines + 1))

        self.linenums.configure(state='normal')
        self.linenums.delete('1.0', 'end')
        self.linenums.insert('1.0', linenums, tags='right')
        self.linenums.configure(state='disabled')

        if self.textbox.yview()[0] != self.textbox.index('end'):
            self.linenums.yview_moveto(self.textbox.index('end'))

        self.linenums.yview_moveto(self.textbox.yview()[0])

    def _update_position(self, event=None):
        pos = self.textbox.index('insert')
        ln, col = pos.split('.')
        self.statusbar.menu['Position'].configure(text=f'{ln}:{col}')

    def open_file(self, file: TextIO):
        self.textbox.insert('1.0', file.read())
        self.statusbar.menu['Encoding'].configure(text=file.encoding)
        self._get_lnend(file)

        self._update_linenums()

    def _get_lnend(self, file: TextIO):
        with open(file.name, 'rb') as file:
            text = file.read()
            if b'\r\n' in text:
                lnend = 'CRLF'
            elif b'\r' in text:
                lnend = 'CR'
            elif b'\n' in text:
                lnend = 'LF'
            self.statusbar.menu['Line Ending'].configure(text=lnend)
