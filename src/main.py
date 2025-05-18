from tkinter import PhotoImage

from customtkinter import *
from picea import *
import sys

set_default_color_theme('../res/theme/default.json')
set_appearance_mode('system')

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title('Picea Notepad')
        if sys.platform.startswith('win'):
            self.iconbitmap('../res/icon.ico')
        else:
            self.iconphoto(False, PhotoImage(file='../res/icon.png'))
        self.geometry('800x600')

        self.menubar = Menubar(self, fg_color=('white', '#000000'))
        self.menubar.pack(side='top', anchor='nw', fill='x')

        self.menubar.add_cascade('File')
        self.menubar.add_cascade('Edit')
        self.menubar.add_cascade('Help')
        self.menubar.pack_cascades(side='left', ipadx=8)

        self.menubar.add_command('File', label='New', command=self.new_tab)
        self.menubar.add_separator('File')
        self.menubar.add_command('File', label='Exit', command=exit)

        self.tabview = CTkTabview(self, anchor='nw', fg_color=('#e0e0e0', '#060606'))
        self.tabview.pack(side='bottom', fill='both', expand=True)

        self.tabl = dict()
        self.welcome_page()

        self.bind('<Control-N>', self.new_tab)
        self.bind('<Control-n>', self.new_tab)

    def welcome_page(self):
        self.tabview.add('Welcome')
        welcome_page = WelcomePage(self.tabview.tab('Welcome'))
        welcome_page.add(CTkLabel(welcome_page, text='\nPicea Notepad\n', font=CTkFont(size=36)))
        welcome_page.add(CTkLabel(welcome_page, text='Start', font=CTkFont(size=24)))
        welcome_page.add(CTkButton(welcome_page, text='New', anchor='w', command=self.new_tab))
        welcome_page.add(CTkButton(welcome_page, text='Open', anchor='w'))
        welcome_page.add(CTkLabel(welcome_page, text='Recent', font=CTkFont(size=24)))
        welcome_page.add(CTkButton(welcome_page, anchor='w'))
        welcome_page.add(CTkButton(welcome_page, anchor='w'))
        welcome_page.add(CTkButton(welcome_page, anchor='w'))
        welcome_page.cfg_buttons(anchor='w', fg_color='transparent', hover_color=("#e0e0e0", "#242424"))
        welcome_page.pack_all(anchor='nw', pady=3, padx=24)
        welcome_page.pack(fill='both', expand=True)

    def new_tab(self, event=None, **kwargs):
        if 'name' in kwargs:
            name = kwargs['name']
        else:
            name = 'New'
        try:
            self.tabview.add(name)
            self.tabl[name] = dict()
            self.tabl[name]['count'] = 0
        except ValueError:
            self.tabl[name]['count'] += 1
            name = f'{name} ({self.tabl[name]['count']})'
            self.tabview.add(name)
        self.tabl[name]['content'] = Textbox(self.tabview.tab(name), fg_color=('#e0e0e0', '#060606'))
        if sys.platform.startswith('win'):
            self.tabl[name]['content'].textbox.configure(font=CTkFont(family='Cascadia Mono', size=14))
            self.tabl[name]['content'].linenums.configure(font=CTkFont(family='Cascadia Mono', size=14))
        self.tabl[name]['content'].pack(fill='both', expand=True)
        self.tabview.set(name)

if __name__ == '__main__':
    App().mainloop()