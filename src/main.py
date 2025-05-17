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

        self.menubar.add_cascade('File', ['New', 'Open', 'Save', '***', 'Exit'])
        self.menubar.add_cascade('Edit', ['Undo', '***', 'Settings'])
        self.menubar.add_cascade('Help', ['About'])

        self.tabview = CTkTabview(self, anchor='nw', fg_color=('#c0c0c0', '#060606'))
        self.tabview.pack(side='bottom', fill='both', expand=True)

        self.tab_count = 0
        self.tabl = dict()
        self.welcome_page()

        self.bind('<Control-N>', self.new_tab)
        self.bind('<Control-n>', self.new_tab)

    def welcome_page(self):
        self.tabview.add('Welcome')
        welcome_page = WelcomePage(self.tabview.tab('Welcome'))
        welcome_page.add(CTkLabel(welcome_page, text='Start', font=CTkFont(size=24)))
        welcome_page.add(CTkButton(welcome_page, text='New', anchor='w'))
        welcome_page.add(CTkButton(welcome_page, text='Open', anchor='w'))
        welcome_page.add(CTkLabel(welcome_page, text='Recent', font=CTkFont(size=24)))
        welcome_page.add(CTkButton(welcome_page, anchor='w'))
        welcome_page.add(CTkButton(welcome_page, anchor='w'))
        welcome_page.add(CTkButton(welcome_page, anchor='w'))
        welcome_page.pack_all(anchor='nw', pady=3)
        welcome_page.pack(fill='both', expand=True, padx=24, pady=12)

    def new_tab(self, event, *args):
        if 'name' in args:
            name = args[2]
        else:
            self.tab_count += 1
            name = f'New-{self.tab_count}'
        self.tabview.add(name)
        self.tabl[name] = Textbox(self.tabview.tab(name), fg_color=('#c0c0c0', '#060606'))
        if sys.platform.startswith('win'):
            self.tabl[name].textbox.configure(font=CTkFont(family='Cascadia Mono', size=14))
            self.tabl[name].linenums.configure(font=CTkFont(family='Cascadia Mono', size=14))
        self.tabl[name].pack(fill='both', expand=True)
        self.tabview.set(name)

if __name__ == '__main__':
    App().mainloop()