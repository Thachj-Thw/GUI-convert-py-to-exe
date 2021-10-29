import tkinter as tk
from tkinter import ttk
import os


class AddData(tk.Frame):
    """
    AddData     (Frame)
        - all       (LabelFrame)
            - listbox   (Listbox)
        - buttons   (Frame)
            - add       (Button)
            - add_all   (Button)
            - rm        (Button)
            - rm_all    (Button)
        - add       (LabelFrame)
            - listbox   (Listbox)
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        self.frame = tk.LabelFrame(self, text="Add data", bg=master["bg"])
        self.all = DataFrame(self.frame, text="All data", bd=0)
        self.add = DataFrame(self.frame, text="Data added", bd=0)
        self.buttons = Buttons(self.frame)
        self.buttons.add["command"] = self.on_add
        self.buttons.add_all["command"] = self.on_addall
        self.buttons.rm["command"] = self.on_rm
        self.buttons.rm_all["command"] = self.on_rmall
        self.allfile = []
        self.addfile = []

        self.all.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.X)
        self.buttons.pack(side=tk.LEFT, fill=tk.Y, pady=35)
        self.add.pack(side=tk.RIGHT, padx=5, pady=10, fill=tk.X)
        self.frame.pack()
        self.pack(padx=5, pady=5)

    def add_all(self, folder):
        self.all.listbox.delete(0, tk.END)
        self.add.listbox.delete(0, tk.END)
        self.allfile.clear()
        self.addfile.clear()
        for f in os.listdir(folder):
            self.all.listbox.insert(tk.END, f)
            self.allfile.append(f)

    def remove_all(self):
        self.all.listbox.delete(0, tk.END)
        self.add.listbox.delete(0, tk.END)
        self.allfile.clear()
        self.addfile.clear()

    def get_add(self):
        return self.addfile

    def on_add(self):
        index = self.all.listbox.curselection()[::-1]
        for i in index:
            file = self.allfile.pop(i)
            self.add.listbox.insert(tk.END, file)
            self.addfile.append(file)
            self.all.listbox.delete(i)

    def on_addall(self):
        for f in self.allfile:
            self.addfile.append(f)
            self.add.listbox.insert(tk.END, f)
        self.allfile.clear()
        self.all.listbox.delete(0, tk.END)

    def on_rm(self):
        index = self.add.listbox.curselection()[::-1]
        for i in index:
            file = self.addfile.pop(i)
            self.allfile.append(file)
            self.all.listbox.insert(tk.END, file)
            self.add.listbox.delete(i)

    def on_rmall(self):
        for f in self.addfile:
            self.allfile.append(f)
            self.all.listbox.insert(tk.END, f)
        self.addfile.clear()
        self.add.listbox.delete(0, tk.END)


class DataFrame(tk.LabelFrame):
    """Custom listbox show project's files"""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        frame = tk.Frame(self)
        style = ttk.Style()
        style.layout('arrowless.Vertical.TScrollbar',
                     [('Vertical.Scrollbar.trough', {
                         'sticky': 'ns',
                         'children': [('Vertical.Scrollbar.thumb', {
                                          'expand': '1',
                                          'sticky': 'nswe'})]})])
        style.configure("arrowless.Vertical.TScrollbar",
                        troughcolor="#ffffff",
                        troughrelief="flat",
                        troughborderwidth=0,
                        width=8,
                        relief="flat")
        self.scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, style="arrowless.Vertical.TScrollbar")
        self.listbox = tk.Listbox(frame, yscrollcommand=self.scrollbar.set, selectmode=tk.EXTENDED,
                                  bd=0, width=28, height=8)
        self.scrollbar["command"] = self.listbox.yview

        frame.pack()
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT)


class Buttons(tk.Frame):
    """frame have 4 buttons add, add all, remove, remove all"""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        add = tk.Frame(self, bg=master["bg"])
        remove = tk.Frame(self, bg=master["bg"])
        self.add = HoverButton(add, text="Add")
        self.add_all = HoverButton(add, text="Add all")
        self.rm = HoverButton(remove, text="Remove")
        self.rm_all = HoverButton(remove, text="Remove all")

        add.pack(side=tk.TOP)
        remove.pack(side=tk.BOTTOM)
        self.add.pack(side=tk.TOP)
        self.add_all.pack(side=tk.BOTTOM)
        self.rm.pack(side=tk.TOP)
        self.rm_all.pack(side=tk.BOTTOM)


class HoverButton(tk.Button):
    """Custom button"""
    def __init__(self, master, **kwargs):
        super().__init__(master, font="Calibri 10", bg=master["bg"], bd=0,  width=9, activebackground="#4ee5ed",
                         **kwargs)
        self.default = self["bg"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, _):
        self["bg"] = self["activebackground"]

    def on_leave(self, _):
        self["bg"] = self.default
