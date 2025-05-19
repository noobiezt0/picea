from customtkinter import CTkFrame, CTkTextbox, CTkScrollbar
from pinaceae.menu import Menubar

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
            width=48,
            text_color='#969696',
        )

        self.statusbar = Menubar(self, height=16, fg_color='transparent')
        self.statusbar.pack(side='bottom', fill='x', padx=3, pady=(0, 3))
        self.statusbar.add_cascade('Enc')
        self.statusbar.add_cascade('CRLF')
        self.statusbar.add_cascade('Pos')
        self.statusbar.pack_cascades(side='right', ipadx=8)

        self._vscrollbar.pack(side='right', fill='y', padx=3, pady=(0, 16))
        self._hscrollbar.pack(side='bottom', fill='x', padx=3, pady=(0, 6))
        self.textbox.pack(side='right', fill='both', pady=(0, 3), expand=True)
        self.linenums.pack(side='left', fill='y', padx=3, pady=(0, 3))

        self.textbox.bind('<<Modified>>', self._update_linenums)
        self.textbox.bind('<Button-4>', self._update_linenums)
        self.textbox.bind('<Button-5>', self._update_linenums)
        self.textbox.bind('<KeyRelease>', self._update_position)

        self._update_linenums()
        self._update_position()

    def _update_linenums(self, event=None):
        self.textbox.edit_modified(False)

        lines = self.textbox.get('1.0', 'end-1c').count('\n') + 1
        linenums = '\n'.join(str(i) for i in range(1, lines + 1))

        self.linenums.configure(state='normal')
        self.linenums.delete('1.0', 'end')
        self.linenums.insert('1.0', linenums)
        self.linenums.configure(state='disabled')

        self.linenums.yview_moveto(self.textbox.yview()[0])

    def _update_position(self, event=None):
        pos = self.textbox.index('insert')
        ln, col = pos.split('.')
        self.statusbar.menu['Pos'].configure(text=f"{ln}:{col}")
