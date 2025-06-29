import darkdetect
from tkdev import *


class Editor(DevWindow):
    def __init__(self):
        super(Editor, self).__init__()
        self.minsize(860, 480)
        self.mica(Dark)
        from sv_ttk import use_dark_theme, use_light_theme
        self.theme = "dark"
        use_dark_theme()
        self.set_menubar()
        self.set_editor()
        self.set_statusbar()

    def set_menubar(self):
        self.menubar = tk.Frame(self, background="#000000")
        self.menu_file = tk.Button(self.menubar, text="文件", font=("微软雅黑", 10),
                                   background="#000000", foreground="#ffffff",
                                   activebackground="#101010", activeforeground="#ffffff",
                                   borderwidth=0, relief=tk.FLAT)
        self.menu_file.pack(side=tk.LEFT, padx=3, pady=3)
        self.menubar.pack(fill=tk.X, side=tk.TOP)

    def set_editor(self):
        self.editor = tk.Text(self, border=0, height=10, width=10, background="#070707")
        self.editor.pack(fill=tk.BOTH, expand=tk.YES, side=tk.TOP, ipadx=10, ipady=10)

    def set_statusbar(self):
        self.status = DevStatusBar(self, sizegrip=False)
        self.status.status.configure(background="#000000")
        self.status.configure(background="#000000")
        self.status.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == '__main__':
    Root = Editor()
    Root.mainloop()
