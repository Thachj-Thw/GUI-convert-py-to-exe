import tkinter as tk


class Convert(tk.Frame):
    """
    Convert (Frame)
        - button (Button)
        - label (Label)
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        self.default = master["bg"]
        self.button = tk.Button(self, text="Convert", bg=self.default, bd=0, font="Bahnschrift 15",
                                activebackground="#4ee5ed", width=13, height=1)
        self.label = tk.Label(self, text="", bg=self.default, font="Calibri 10")
        self.button.pack(pady=15)
        self.label.pack()
        self.pack(pady=5, fill=tk.X)
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

    def set_command(self, func):
        self.button["command"] = func

    def set_text(self, text, color):
        self.label["text"] = text
        self.label["fg"] = color

    def disable(self):
        self.button["state"] = tk.DISABLED

    def enable(self):
        self.button["state"] = tk.NORMAL

    def on_enter(self, _):
        if self.button["state"] != tk.DISABLED:
            self.button["bg"] = self.button["activebackground"]

    def on_leave(self, _):
        self.button["bg"] = self.default
