import tkinter as tk


class Info(tk.Frame):
    """Show Pyinstaller version"""
    def __init__(self, master, version, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        label = tk.Label(self, text="Pyinstaller version " + version, bg=master["bg"], font="Calibri 8")
        label.pack(side=tk.RIGHT, padx=10, pady=5)
        self.pack(fill=tk.X)
