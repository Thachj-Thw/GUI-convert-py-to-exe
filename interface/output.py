import tkinter as tk
import os


class OutFile(tk.Frame):
    """
    OutFile (Frame)
        - fout (LabelFrame)
            - (label "path")
            - entry (Entry)
            - path (StringVar)
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        self.fout = FrameOut(self)
        self.pack(fill=tk.X)

    def set_command(self, func):
        self.fout.button["command"] = func

    def set_path(self, path):
        self.fout.path.set(path)

    def get_path(self):
        return os.path.normcase(self.fout.entry.get())


class FrameOut(tk.LabelFrame):
    """LabelFrame name Folder put your app"""
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Folder put your app", bg=master["bg"], **kwargs)
        label = tk.Label(self, text="Path:", bg=master["bg"], font="Calibri 10")
        self.path = tk.StringVar(value="")
        self.entry = tk.Entry(self, textvariable=self.path, width=50, bg="#ffffff", font="Calibri 10", bd=0)
        self.default = master["bg"]
        self.button = tk.Button(self, text="Change", activebackground="#4ee5ed", width=6, font="Calibri 10",
                                bg=self.default, bd=0)

        label.pack(side=tk.LEFT, padx=5, pady=5)
        self.entry.pack(side=tk.LEFT, pady=5)
        self.button.pack(side=tk.LEFT, padx=5)
        self.pack(side=tk.LEFT, padx=5, pady=10)
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

    def on_enter(self, _):
        self.button["bg"] = self.button["activebackground"]

    def on_leave(self, _):
        self.button["bg"] = self.default
