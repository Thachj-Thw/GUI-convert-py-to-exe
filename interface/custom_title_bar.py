import tkinter as tk
import tkinter.ttk as ttk
from ctypes import windll

GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
DARKGRAY = "#A9A9A9"
LGRAY = "#545454"
DGRAY = "#242424"
RGRAY = "#2e2e2e"
WHITE = "#ffffff"
LWHITE = "#808080"
RED = "#ec1313"


def set_appwindow(root):
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
    root.withdraw()
    root.deiconify()


class HoverButton(tk.Button):
    def __init__(self, master, **kwargs):
        tk.Button.__init__(self, master, **kwargs)
        self.default = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, _):
        self["background"] = self["activebackground"]

    def on_leave(self, _):
        self["background"] = self.default


class TitleBar(tk.Frame):
    def __init__(self, master, title="App - title", **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.master = master
        self.master.overrideredirect(True)
        # set_appwindow(master)
        self.name_app = title
        self.title = tk.Label(self, text=self.name_app, bg=self["bg"], fg=LWHITE)
        self.x_button = HoverButton(self, text="X", bg=self["bg"], font="Calibri 13", fg=LWHITE, bd=0, width=3,
                                    activebackground=RED, command=self.master.quit)
        self.r_button = HoverButton(self, text="❒", bg=self["bg"], font="Calibri 13", fg=LWHITE, bd=0, width=3,
                                    activebackground=LGRAY)
        self.m_button = HoverButton(self, text="-", bg=self["bg"], font="Cambria_Math 13", fg=LWHITE, bd=0, width=3,
                                    activebackground=LGRAY, command=self.minimize)
        self.master.update()
        self.title.pack(side=tk.LEFT, padx=10)
        self.x_button.pack(side=tk.RIGHT, fill=tk.Y)
        self.r_button.pack(side=tk.RIGHT, fill=tk.Y)
        self.m_button.pack(side=tk.RIGHT, fill=tk.Y)
        self.pack(side=tk.TOP, fill=tk.X)
        self.bind("<Button-1>", self.on_hold)
        self.bind("<B1-Motion>", self.on_move)
        self.x_mouse = 0
        self.y_mouse = 0
        self.bind("<Map>", self.mapped)

    def on_hold(self, e):
        self.x_mouse = e.x_root - self.master.winfo_rootx()
        self.y_mouse = e.y_root - self.master.winfo_rooty()

    def on_move(self, e):
        self.master.geometry(f"+{e.x_root - self.x_mouse}+{e.y_root - self.y_mouse}")

    def minimize(self):
        self.master.update_idletasks()
        self.master.overrideredirect(False)
        self.master.iconify()

    def mapped(self, _):
        self.master.update_idletasks()
        self.master.overrideredirect(True)
        self.master.deiconify()
