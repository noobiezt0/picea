from customtkinter import *
from picea import *

set_default_color_theme('../res/theme/default.json')
set_appearance_mode('system')

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title('Picea Notepad')
        self.iconbitmap('../res/icon.ico')
        self.geometry('800x600')

        self.tabview = CTkTabview(self, anchor='nw', fg_color=('#c0c0c0', '#000000'))
        self.tabview.pack(side='bottom', fill='both', expand=True)

        self.tabview.add('New')
        self.textbox = Textbox(self.tabview.tab('New'), fg_color=('#c0c0c0', '#000000'))
        self.textbox.pack(fill='both', expand=True)

        self.menubar = Menubar(self, fg_color=('white', '#000000'))
        self.menubar.pack(side='top', anchor='nw', fill='x')

        self.menubar.add_cascade('File', ['New', 'Open', 'Save', '***', 'Exit'])
        self.menubar.configure()
        self.menubar.add_cascade('Edit', ['Undo', '***', 'Settings'])
        self.menubar.add_cascade('Help', ['About'])

if __name__ == '__main__':
    App().mainloop()