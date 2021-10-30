import tkinter as tk
from tkinter import filedialog
import os


class InFile(tk.Frame):
    """
    InFile (Frame)
        - fname (Frame)
            - (label "name")
            - entry (Entry)
            - name (StringVar)
        - fpath (LabelFrame)
            - (label "path")
            - entry (Entry)
            - path (StringVar)
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        frame = tk.Frame(self, bg=master["bg"])
        self.fname = FrameName(frame)
        self.fpath = FramePath(frame)
        frame.pack(side=tk.LEFT, padx=5, pady=10)
        self.pack(fill=tk.X)

    def set_command(self, func):
        self.fpath.button["command"] = func

    def set_trace(self, func):
        self.fpath.path.trace_variable("w", lambda n, i, m: func())

    def set_path(self, path):
        self.fpath.path.set(path)
        if not self.fname.name.get():
            self.fname.name.set(os.path.splitext(os.path.basename(path))[0])

    def get_path(self):
        return self.fpath.entry.get()

    def get_name(self):
        return self.fname.entry.get()


class FrameName(tk.Frame):
    """Input Project's name"""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        label = tk.Label(self, text="Name:", bg=self["bg"], font="Calibri 10")
        self.name = tk.StringVar(value="")
        self.entry = tk.Entry(self, textvariable=self.name, bg="#ffffff", bd=0, font="Calibri 10", width=20)
        label.pack(side=tk.LEFT, padx=5)
        self.entry.pack(side=tk.LEFT, padx=5, pady=10)
        self.pack(side=tk.TOP, fill=tk.X)


class FramePath(tk.LabelFrame):
    """LabelFrame name File Convert"""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], text="File Convert", **kwargs)
        label = tk.Label(self, text="Path:", bg=self["bg"], font="Calibri 10")
        self.path = tk.StringVar(value="")
        self.entry = tk.Entry(self, textvariable=self.path, bg="#ffffff", bd=0, font="Calibri 10", width=50)
        self.default = master["bg"]
        self.button = tk.Button(self, text="Select", width=6, activebackground="#4ee5ed", bg=self.default, bd=0,
                                font="Calibri 10", command=self.on_click)
        label.pack(side=tk.LEFT, padx=5, pady=5)
        self.entry.pack(side=tk.LEFT, pady=5)
        self.button.pack(side=tk.LEFT, padx=5)
        self.pack(side=tk.BOTTOM, fill=tk.X)
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

    def on_click(self):
        path = filedialog.askopenfilename(title="Chose a python file",
                                          filetypes=(("Python file", ".py .pyw"), ("All file", "*.*")))
        if path:
            self.path.set(os.path.normpath(path))

    def on_enter(self, _):
        self.button["bg"] = self.button["activebackground"]

    def on_leave(self, _):
        self.button["bg"] = self.default
