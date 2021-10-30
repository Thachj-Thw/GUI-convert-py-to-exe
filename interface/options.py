import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import os


class Options(tk.Frame):
    """
    Options (Frame)
        - option_check (Frame)
            - cb_onfile (custom checkbox)
            - cb_noconsole (custom checkbox)
            - cb_admin (custom checkbox)
        - option_icon (Frame)
            - image (Label)
            - menu (Combobox)
    """
    def __init__(self, master, icon_default: tuple, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        self.option_check = CheckBoxOptions(self)
        self.icon_windowed = icon_default[0]
        self.icon_console = icon_default[1]
        self.path = tk.StringVar(value="")
        self.option_icon = Icon(self)
        self.option_icon.image["image"] = self.icon_windowed
        self.option_icon.menu.bind("<<ComboboxSelected>>", self.icon_changed)
        self.option_check.cb_noconsole["command"] = self.checkbox_changed
        self.pack(fill=tk.X)

    def onfile(self):
        return self.option_check.onefile.get()

    def noconsole(self):
        return self.option_check.noconsole.get()

    def admin(self):
        return self.option_check.admin.get()

    def icon_changed(self, _e):
        option = self.option_icon.option.get()
        if option == "Default":
            self.path.set("")
            if self.option_check.noconsole.get():
                self.option_icon.image["image"] = self.icon_windowed
            else:
                self.option_icon.image["image"] = self.icon_console
        elif option == "None":
            self.path.set("NONE")
            self.option_icon.image["image"] = ""
        else:
            path = filedialog.askopenfilename(title="Select a icon file", filetypes=(("Icon file", ".ico"),))
            if path:
                self.path.set(os.path.normpath(path))
                img = ImageTk.PhotoImage(Image.open(self.path.get()).resize((32, 32)))
                self.option_icon.image["image"] = img
                self.option_icon.image.image = img
            else:
                if self.path.get():
                    self.option_icon.option.set("None")
                else:
                    self.option_icon.option.set("Default")

    def checkbox_changed(self):
        if self.option_check.noconsole.get():
            self.option_icon.image["image"] = self.icon_windowed
        else:
            self.option_icon.image["image"] = self.icon_console

    def get_path(self):
        return self.path.get()

    def disable_noconsole(self):
        self.option_check.noconsole.set(value=1)
        self.option_check.cb_noconsole.disable()
        if self.option_icon.option.get() == "Default":
            self.option_icon.image["image"] = self.icon_windowed

    def enable_noconsole(self):
        self.option_check.cb_noconsole.enable()


class CheckBoxOptions(tk.LabelFrame):
    """3 options pyinstaller: onefile, noconsole and run as administrator"""
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Options", bg=master["bg"], **kwargs)
        frame1 = tk.Frame(self, bg=master["bg"])
        frame2 = tk.Frame(self, bg=master["bg"])
        frame3 = tk.Frame(self, bg=master["bg"])
        self.onefile = tk.IntVar(value=1)
        self.noconsole = tk.IntVar(value=1)
        self.admin = tk.IntVar(value=1)
        self.cb_onefile = HoverCheckButton(frame1, text="One file", variable=self.onefile)
        self.cb_noconsole = HoverCheckButton(frame2, text="No console", variable=self.noconsole)
        self.cb_admin = HoverCheckButton(frame3, text="Run as administrator", variable=self.admin)
        self.cb_onefile.pack(side=tk.LEFT)
        self.cb_noconsole.pack(side=tk.LEFT)
        self.cb_admin.pack(side=tk.LEFT)
        frame1.pack(fill=tk.X)
        frame2.pack(fill=tk.X)
        frame3.pack(fill=tk.X)
        self.pack(expand=True, side=tk.LEFT, padx=5, pady=5, fill=tk.X)


class HoverCheckButton(tk.Checkbutton):
    """Custom check button"""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], activebackground=master["bg"], font="Calibri 10", **kwargs)
        self.default = self["fg"]
        self.active = "#6c0094"
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, _):
        self["fg"] = self.active

    def on_leave(self, _):
        self["fg"] = self.default

    def disable(self):
        self["state"] = tk.DISABLED

    def enable(self):
        self["state"] = tk.NORMAL


class Icon(tk.LabelFrame):
    """Show image icon"""
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Icon", bg=master["bg"],  **kwargs)
        self.image = tk.Label(self, text="Icon OS", bg=master["bg"])
        s = ttk.Style()
        master.option_add("*TCombobox*Listbox*Background", master["bg"])
        master.option_add("*TCombobox*Listbox*Foreground", "black")
        master.option_add("*TCombobox*Listbox*selectBackground", "white")
        master.option_add("*TCombobox*Listbox*selectForeground", "black")
        s.theme_create("mytheme", parent="default", settings={
            "TCombobox": {
                "configure": {"fieldbackground": master["bg"],
                              "borderwidth": 1,
                              "bordercolor": "black",
                              "background": master["bg"],
                              "arrowcolor": "black",
                              "arrowsize": 12,
                              "relief": "flat",
                              "padding": 1,
                              "shiftrelief": "flat",
                              "font": ("Calibri", 10)
                              },
                "map": {"selectbackground": [("readonly", master["bg"])],
                        "selectforeground": [("readonly", "black")],
                        "background": [("readonly", master["bg"])]}}})
        s.theme_use("mytheme")
        options = ("Default", "None", "Option")
        self.option = tk.StringVar(value=options[0])
        self.menu = ttk.Combobox(self, textvariable=self.option, values=options, width=10)
        self.menu["state"] = "readonly"
        self.image.pack()
        self.menu.pack(side=tk.BOTTOM, padx=5, pady=5)
        self.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
