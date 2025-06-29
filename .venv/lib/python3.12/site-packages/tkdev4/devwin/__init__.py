from tkdev4 import tk, window_embed, DevWindow, DevToplevel


class WinMDIWindow(tk.Frame):
    def __init__(self, master: tk.Tk):
        super(WinMDIWindow, self).__init__(master=master)

    def add_child(self, child: tk.Toplevel) -> None:
        window_embed(self, child, False)

    def add(self) -> tk.Toplevel:
        def embed():
            child = DevToplevel(self)
            child.geometry(f"{self.winfo_width()-15}x{self.winfo_height()-15}+0+0")
            window_embed(self, child, False)
            return child
        self.after(1, embed)

    def show(self):
        self.pack(fill="both", expand="yes")

    def preview(self, child):
        self.after(2, child.mainloop())


class WinMDIChild(DevToplevel):
    def __init__(self, master: tk.Tk = None, title: str = ""):
        super(WinMDIChild, self).__init__(master=master, title=title)

