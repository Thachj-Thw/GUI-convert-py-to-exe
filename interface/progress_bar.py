import tkinter as tk
from tkinter import ttk


class ProgressBar(tk.Frame):
    """
    ProgressBar (Frame)
        - (frame image convert py to exe)
        - bar (Progressbar)
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("My.Horizontal.TProgressbar",
                        borderwidth=0,
                        troughcolor="#ffffff",
                        background="#54f6ff")
        self.bar = ttk.Progressbar(self, length=450, orient=tk.HORIZONTAL, style="My.Horizontal.TProgressbar")
        frame = tk.Frame(self, bg=master["bg"])
        tk.Label(frame, text="Loading...", font="Bahnschrift 9", bg=master["bg"], fg="#ffffff").pack(side=tk.LEFT)

        Label(self)
        self.bar.pack(side=tk.BOTTOM)
        frame.pack(fill=tk.X)
        self.pack()

    def set(self, v):
        self.bar["value"] = v


class Label(tk.Frame):
    """Image Convert py to exe"""
    def __init__(self, master, **kwargs):
        super().__init__(master, height=150, bg=master["bg"], **kwargs)
        fg = "#ffffff"
        font = "Calibri"
        font_size = 40
        label1 = tk.Label(self, text="Convert", font=(font, font_size), bg=master["bg"], fg=fg)
        label2 = tk.Label(self, text="py", font=(font, font_size, "bold"), bg=master["bg"], fg=fg)
        label3 = tk.Label(self, text="to", font=(font, font_size), bg=master["bg"], fg=fg)
        label4 = tk.Label(self, text="exe", font=(font, font_size, "bold"), bg=master["bg"], fg=fg)

        x, y = 40, 8
        x2, y2 = x + 180, y + 70
        label1.place(x=x, y=y)
        label2.place(x=x+180, y=y)
        label3.place(x=x2, y=y2)
        label4.place(x=x2+55, y=y2)
        self.pack(fill=tk.BOTH, expand=True)
