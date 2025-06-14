from customtkinter import *

from abies import Layout

from picea.textbox import TextboxFrame
from picea.menubar import Menubar

from tkinter import PhotoImage
from tkinter.filedialog import askopenfilename

import sys
import os

class App(CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title('Picea Notepad')
        if sys.platform.startswith('win'):
            self.iconbitmap('../res/icon/icon.ico')
        else:
            self.iconphoto(False, PhotoImage(file='../res/icon/icon.png'))
        self.geometry('800x600')

        self.layouts = dict()

        self.tabview = CTkTabview(self, anchor='nw', fg_color=('white', 'black'))
        self.tabs = dict()

        self.menubar = Menubar(self, fg_color=('white', 'black'))
        self.menubar.add_cascade('File')
        self.menubar.add_cascade('Edit')
        self.menubar.add_cascade('Help')

        self.menubar.add_command('File', label='New', command=self.create_tab)
        self.menubar.add_command('File', label='Open')
        self.menubar.add_separator('File')
        self.menubar.add_command('File', label='Exit', command=exit)

        self.menubar.add_command('Help', label='About')

        for layout in os.listdir('../res/layouts/'):
            with open(f'../res/layouts/{layout}') as layoutf:
                self.layouts[layout.removesuffix('.json')] = layoutf.read()

        self.menubar.pack(side='top', anchor='nw', fill='x')
        self.menubar.pack_cascades(side='left', ipadx=8)

        self.tabview.pack(side='bottom', fill='both', expand=True)
        self.create_tab(None, name='Welcome')

        self.bind('<Control-n>', self.create_tab)
        self.bind('<Control-N>', self.create_tab)
        self.bind('<Control-o>', self.open_file)
        self.bind('<Control-O>', self.open_file)

    def create_tab(self, event=None, **kwargs) -> None:
        if 'name' in kwargs:
            name = kwargs['name']
        else:
            name = 'New'

        if name not in self.tabs:
            self.tabs[name] = dict()

        try:
            self.tabview.add(name)
            if 'count' not in self.tabs[name]:
                self.tabs[name]['count'] = 0
        except ValueError:
            self.tabs[name]['count'] += 1
            name = f'{name} ({self.tabs[name]['count']})'
            self.tabs[name] = dict()
            self.tabview.add(name)

        if name == 'Welcome':
            self.tabs[name]['frame'] = CTkFrame(self.tabview.tab(name))
            layout = Layout(self.tabs[name]['frame'])
            layout.load(self.layouts['welcome'])
            layout.widgets['Button-New'].configure(command=self.create_tab)
            layout.widgets['Button-Open'].configure(command=self.open_file)
            CTkButton(self.tabs[name]['frame'], anchor='nw')
            CTkButton(self.tabs[name]['frame'], anchor='nw')
            CTkButton(self.tabs[name]['frame'], anchor='nw')
            self.tabs[name]['frame'].pack(fill='both', expand=True)
        else:
            self.tabs[name]['frame'] = TextboxFrame(self.tabview.tab(name), fg_color=('white', 'black'))
            self.tabs[name]['frame'].textbox.configure(font=CTkFont('Cascadia Mono'))
            self.tabs[name]['frame'].linenums.configure(font=CTkFont('Cascadia Mono'))

        self.tabs[name]['frame'].pack(fill='both', expand=True)
        self.tabview.set(name)

        self.tabview.tab(name).bind('<Button-2>', self.close_tab)

    def close_tab(self, event=None) -> None:
        self.tabview.delete(self.master.cget('-name'))

    def open_file(self, event=None) -> None:
        fp = askopenfilename()
        if not (fp in self.tabs):
            try:
                with open(fp) as file:
                    self.create_tab(None, name=fp)
                    self.tabs[fp]['frame'].open_file(file)
            except (FileNotFoundError, TypeError):
                return
        else:
            self.tabview.set(fp)

if __name__ == '__main__':
    set_default_color_theme('../res/theme.json')
    set_appearance_mode('dark')
    App().mainloop()