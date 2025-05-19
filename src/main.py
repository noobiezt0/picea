from customtkinter import *

from pinaceae.abies.abies import abies
from pinaceae.textbox import TextboxFrame
from pinaceae.menu import Menubar

from tkinter import PhotoImage

import sys
import os

set_default_color_theme('../res/themes/default.json')
set_appearance_mode('system')

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title('Picea Notepad')
        if sys.platform.startswith('win'):
            self.iconbitmap('../res/icon/icon.ico')
        else:
            self.iconphoto(False, PhotoImage(file='../res/icon/icon.png'))
        self.geometry('800x600')

        self.layouts = dict()

        self.tabview = CTkTabview(self, anchor='nw', fg_color=('#e0e0e0', 'black'))
        self.tabs = dict()

        self.menubar = Menubar(self, fg_color=('white', 'black'))
        self.menubar.add_cascade('File')
        self.menubar.add_cascade('Edit')
        self.menubar.add_cascade('Help')

        self.menubar.add_command('File', label='New', command=self.new_tab, accelerator='Ctrl+N')
        self.menubar.add_command('File', label='Open', accelerator='Ctrl+O')
        self.menubar.add_separator('File')
        self.menubar.add_command('File', label='Exit', command=exit)

        self.menubar.add_command('Help', label='About')

        layouts = os.listdir('../res/layouts/')

        for layout in layouts:
            with open(f'../res/layouts/{layout}') as layoutf:
                self.layouts[layout.removesuffix('.json')] = layoutf.read()

        self.menubar.pack(side='top', anchor='nw', fill='x')
        self.menubar.pack_cascades(side='left', ipadx=8)

        self.tabview.pack(side='bottom', fill='both', expand=True)
        self.new_tab(None, name='Welcome')

        self.bind('<Control-n>', self.new_tab)

    def new_tab(self, event=None, **kwargs):
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
            layout = abies(self.tabs[name]['frame'])
            layout.load(self.layouts['welcome'])
            layout.widgets['Button-New'].configure(command=self.new_tab)
            CTkButton(self.tabs[name]['frame'], anchor='nw')
            CTkButton(self.tabs[name]['frame'], anchor='nw')
            CTkButton(self.tabs[name]['frame'], anchor='nw')
            self.tabs[name]['frame'].pack(fill='both', expand=True)
        else:
            self.tabs[name]['frame'] = TextboxFrame(self.tabview.tab(name), fg_color=('#e0e0e0', 'black'))
            self.tabs[name]['frame'].textbox.configure(font=CTkFont('Consolas', size=16))
            self.tabs[name]['frame'].linenums.configure(font=CTkFont('Consolas', size=16))

        self.tabs[name]['frame'].pack(fill='both', expand=True)
        self.tabview.set(name)

if __name__ == '__main__':
    App().mainloop()