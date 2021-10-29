import tkinter as tk
from tkinter import ttk
import time


class Converting(tk.Frame):
    """Progress bar bottom"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        style = ttk.Style()
        style.configure("My.Horizontal.TProgressbar", borderwidth=0, troughcolor="#ffffff", background="#54f6ff")
        style.configure("Suc.Horizontal.TProgressbar", borderwidth=0, troughcolor="#ffffff", background="#43ff36")
        style.configure("Fail.Horizontal.TProgressbar", borderwidth=0, troughcolor="#ffffff", background="#ff3636")
        self.bar = ttk.Progressbar(self, length=466, orient=tk.HORIZONTAL, style="My.Horizontal.TProgressbar")
        self.bar.pack()
        self.pack()

    def run_animation(self, boolean: tk.BooleanVar):
        self.bar["mode"] = "indeterminate"
        self.bar["style"] = "My.Horizontal.TProgressbar"
        while boolean.get():
            time.sleep(0.02)
            self.bar["value"] = (self.bar["value"] + 1) % 200
            self.update_idletasks()
            self.update()

    def convert_suc(self):
        self.bar["mode"] = "determinate"
        self.bar["style"] = "Suc.Horizontal.TProgressbar"
        self.bar["value"] = 100

    def convert_fail(self):
        self.bar["mode"] = "determinate"
        self.bar["style"] = "Fail.Horizontal.TProgressbar"
        self.bar["value"] = 100
