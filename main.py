# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from resource_path import resource_path
import os
import _thread
import shutil
import subprocess
import PyInstaller

path = os.path.normcase(resource_path.path())

# Init
root = Tk()
root.title("Convert py to exe")
root_icon = f"{path}\\icon\\pyinstaller.ico"
root.iconbitmap(root_icon)
root.geometry("345x450")
root.minsize(345, 450)
root.maxsize(345, 450)

# import image
icon_windowed = ImageTk.PhotoImage(Image.open(f"{path}\\icon\\windowed.ico").resize((32, 32)))
icon_console = ImageTk.PhotoImage(Image.open(f"{path}\\icon\\console.ico").resize((32, 32)))

# Global variable
file_name = StringVar()
lst_data = []
lst_add = []
opened = BooleanVar(value=False)
op_tutorial = BooleanVar(value=False)
add_win = None


class WinAddData:
    def __init__(self, master):
        # init window add data
        self.win_add = Toplevel(master)
        self.win_add.title("Add data")
        self.win_add.iconbitmap(root_icon)
        self.win_add.geometry("450x240")
        self.win_add.maxsize(450, 240)
        self.win_add.minsize(450, 240)

        # Main frame
        self.frame_main = Frame(self.win_add)
        self.frame_main.grid(padx=30, pady=15)

        # Frame all data
        self.frame_data = LabelFrame(self.frame_main, text="All data", padx=5, pady=10)
        self.frame_data.grid(row=0, column=0, rowspan=4)

        # Frame scrollbar add data
        self.frame_scrollbar_data = Frame(self.frame_data)
        self.scrollbar_data = Scrollbar(self.frame_scrollbar_data, orient=VERTICAL)
        self.frame_scrollbar_data.grid()

        # Listbox all data
        self.list_data = Listbox(self.frame_scrollbar_data, yscrollcommand=self.scrollbar_data.set, selectmode=EXTENDED)
        self.list_data.grid(row=0, column=0)

        for file in lst_data:
            self.list_data.insert(END, file)

        # config scrollbar all data
        self.scrollbar_data.config(command=self.list_data.yview)
        self.scrollbar_data.grid(row=0, column=1, sticky=S + N)

        # Frame data add
        self.frame_add = LabelFrame(self.frame_main, text="Data add", padx=5, pady=10)
        self.frame_add.grid(row=0, column=2, rowspan=4)

        # Frame scrollbar data add
        self.frame_scrollbar_add = Frame(self.frame_add)
        self.scrollbar_add = Scrollbar(self.frame_scrollbar_add, orient=VERTICAL)
        self.frame_scrollbar_add.grid()

        # Listbox data added
        self.list_data_add = Listbox(self.frame_scrollbar_add,
                                     yscrollcommand=self.scrollbar_add.set, selectmode=EXTENDED)
        self.list_data_add.grid(row=0, column=0)

        for file in lst_add:
            self.list_data_add.insert(END, file)

        # config scrollbar all data
        self.scrollbar_add.config(command=self.list_data_add.yview)
        self.scrollbar_add.grid(row=0, column=1, sticky=S + N)

        # Button add
        self.button_add = Button(self.frame_main, text="Add", command=self.add, anchor=S, width=8)
        self.button_add.grid(row=0, column=1, sticky=S, padx=5)

        # Button add all
        self.button_add_all = Button(self.frame_main, text="Add all", command=self.add_all, width=8)
        self.button_add_all.grid(row=1, column=1, padx=5)

        # Button remove
        self.button_remove = Button(self.frame_main, text="Remove", command=self.remove, width=8)
        self.button_remove.grid(row=2, column=1, padx=5)

        # Button remove all
        self.button_remove_all = Button(self.frame_main, text="Remove all", command=self.remove_all, width=8)
        self.button_remove_all.grid(row=3, column=1, sticky=N, padx=5)

        # Button no such file or directory
        self.button_tutorial = Button(self.frame_main, text="[Errno 2] No such file or directory ?",
                                      command=self.tutorial, relief=FLAT)
        self.button_tutorial.grid(row=4, column=1, columnspan=2, sticky=E)

        # Detect close
        self.win_add.protocol('WM_DELETE_WINDOW', self.on_close)

    def add(self):
        for i in reversed(self.list_data.curselection()):
            lst_add.append(lst_data.pop(i))
        self.update_list_data()

    def add_all(self):
        for i in lst_data:
            lst_add.append(i)
        lst_data.clear()
        self.update_list_data()

    def remove(self):
        for i in reversed(self.list_data_add.curselection()):
            lst_data.append(lst_add.pop(i))
        self.update_list_data()

    def remove_all(self):
        for i in lst_add:
            lst_data.append(i)
        lst_add.clear()
        self.update_list_data()

    def update_list_data(self):
        self.list_data.delete(0, END)
        self.list_data_add.delete(0, END)
        var_add_data.set("")
        for i in lst_data:
            self.list_data.insert(END, i)
        for i in lst_add:
            self.list_data_add.insert(END, i)
            var_add_data.set(i + ", " + var_add_data.get())

    def tutorial(self):
        if not op_tutorial.get():
            op_tutorial.set(True)
            WinTutorial(self.win_add)

    def on_close(self):
        opened.set(False)
        self.win_add.destroy()


class WinTutorial:
    def __init__(self, master):
        # init
        self.win_tutorial = Toplevel(master)
        self.win_tutorial.iconbitmap(root_icon)

        self.tutorial_vn = """Nếu bạn gặp lỗi "[Errno 2] No such file or directory" hãy thử:
    - Copy file resource_path.py trong folder resource_path thêm vào project của bạn
    - Import resource_path và thêm resource_path.path() vào đường dẫn tới data
    Ví dụ:
    File gốc
        # Your_script.py

        with open(".\\\\data.txt", mode=r) as data:
            print(data.read())

    Sửa thành
        # Your_script.py
        import resource_path

        with open(resource_path.path() + "\\\\data.txt", mode=r) as data:
            print(data.read())

    """
        self.tutorial_en = """If you get the error "[Errno 2] No such file or directory" try:
    - Copy the resource_path.py file in the resource_path folder and add it to your project
    - Import resource_path and add resource_path.path() to the path to data
    For example:
    Original file
        # Your_script.py

        with open(".\\\\data.txt", mode=r) as data:
            print(data.read())

    Modified to
        # Your_script.py
        import resource_path

        with open(resource_path.path() + "\\\\data.txt", mode=r) as data:
            print(data.read())

    """

        # Choose language
        self.var_lang = StringVar(value="Tiếng Việt")
        self.lang = OptionMenu(self.win_tutorial, self.var_lang, "Tiếng Việt", "English", command=self.option_lang)
        self.lang.pack()

        # Label tutorial
        self.var_tutorial = StringVar(value=self.tutorial_vn)
        Label(self.win_tutorial, textvariable=self.var_tutorial, padx=10, pady=10, justify=LEFT
              ).pack()

        # Detect close
        self.win_tutorial.protocol('WM_DELETE_WINDOW', self.on_close)

    def option_lang(self, value):
        if value == "English":
            self.var_tutorial.set(self.tutorial_en)
        else:
            self.var_tutorial.set(self.tutorial_vn)

    def on_close(self):
        op_tutorial.set(False)
        self.win_tutorial.destroy()


def openfile():
    root.path = filedialog.askopenfilename(
        title="Choose a file",
        filetypes=(("Python file", ".py .pyw"), ("All file", "*.*"))
    )
    if root.path:
        path_input.set(root.path)
        file_py.set(os.path.basename(root.path))
        lst_data.clear()
        lst_add.clear()
        var_add_data.set("")
        for d in os.listdir(os.path.dirname(root.path)):
            if ".py" not in d:
                lst_data.append(d)
        if opened.get():
            add_win.update_list_data()
        b_convert["state"] = ACTIVE
        if ".pyw" in os.path.basename(root.path):
            no_console.set(1)
            cb_no_console["state"] = DISABLED
        else:
            cb_no_console["state"] = NORMAL


def change_output():
    root.path = filedialog.askdirectory(title="Choose a folder")
    if root.path:
        path_output.set(root.path)


def click_convert():
    file_name.set(os.path.basename(path_input.get())[:os.path.basename(path_input.get()).find(".")])
    command = f'pyinstaller --clean --specpath ".\\spec" --distpath "{os.path.normcase(path_output.get())}" '
    if path_icon.get():
        command += f'--icon="{os.path.normcase(path_icon.get())}" '
    for data in lst_add:
        path_add = f"{os.path.dirname(path_input.get())}\\{data}"
        if "." in data:
            command += f'--add-data="{os.path.normcase(path_add)};." '
        else:
            command += f'--add-data="{os.path.normcase(path_add)};{data}" '
    if one_file.get():
        command += "--onefile "
    if no_console.get():
        command += "--noconsole "
    if admin.get():
        command += "--uac-admin "
    command += f'"{os.path.normcase(path_input.get())}"'
    converting.set("Converting...")
    b_convert["state"] = DISABLED
    _thread.start_new_thread(convert, (command,))


def convert(command):
    proc = subprocess.Popen(command, stderr=subprocess.PIPE)
    info_err = ""
    for line in proc.stderr:
        var_console.set(var_console.get() + "\n" + line.decode()[:-4])
        info_err = line.decode()
    err = proc.wait()
    if err:
        converting.set("Failed")
        l_state['fg'] = "red"
        messagebox.showerror("Convert Failed", info_err)
        os.remove(os.path.join("spec", file_name.get() + ".spec"))
    else:
        converting.set("Successfully")
        l_state['fg'] = "green"
        if messagebox.askyesno("Convert successfully", "Completed successfully!\nDo you want delete spec file?"):
            os.remove(os.path.join("spec", file_name.get() + ".spec"))
    shutil.rmtree(os.path.join("build", file_name.get()))
    b_convert["state"] = NORMAL


def option_icon(value):
    if var_icon.get() == "Default":
        path_icon.set("")
        if no_console.get():
            l_icon["image"] = icon_windowed
            l_icon.image = icon_windowed
        else:
            l_icon["image"] = icon_console
            l_icon.image = icon_console
    elif value == " None  ":
        path_icon.set("NONE")
        l_icon["image"] = ''
        l_icon.image = ''
    elif value:
        root.path = filedialog.askopenfilename(
            title="Choose a file",
            filetypes=(("Icon file", ".ico"),)
        )
        if not root.path:
            if path_icon.get():
                var_icon.set(" None  ")
            else:
                var_icon.set("Default")
        else:
            path_icon.set(root.path)
            img = ImageTk.PhotoImage(Image.open(root.path).resize((32, 32)))
            l_icon["image"] = img
            l_icon.image = img


def add_data():
    global add_win
    if not opened.get():
        opened.set(True)
        add_win = WinAddData(root)


# Frame File convert
frame_input = LabelFrame(root, text="File convert", padx=5, pady=5)
frame_input.grid(row=0, column=0, padx=5, pady=5, sticky=W + E)

# Label file convert
path_input = StringVar(value="")
file_py = StringVar(value="Empty")
Label(frame_input, textvariable=file_py, bd=1, relief=SUNKEN, width=30
      ).grid(row=0, column=0, padx=2, pady=2, sticky=W + E)

# Frame Folder put file .exe
frame_output = LabelFrame(root, text="Folder put the file .exe", padx=5, pady=5)
frame_output.grid(row=1, column=0, padx=5, pady=0, sticky=W + E)

# Label folder output
path_output = StringVar(value=".\\dist")
Label(frame_output, textvariable=path_output, bd=1, relief=SUNKEN, width=30, anchor=E
      ).grid(row=1, column=0, padx=2, pady=2, sticky=W + E)

# Check box no console
no_console = IntVar(value=1)
cb_no_console = Checkbutton(root, text="No console", variable=no_console, anchor=W, padx=10, state=NORMAL,
                            command=lambda: option_icon(""))
cb_no_console.grid(row=3, column=0, sticky=W + E)

# Check box one file
one_file = IntVar(value=1)
Checkbutton(root, text="One file", variable=one_file, anchor=W, padx=10, pady=5
            ).grid(row=2, column=0, sticky=W + E)

# Check box run as administrator
admin = IntVar(value=0)
Checkbutton(root, text="Run as administrator", variable=admin, anchor=W, padx=10, pady=5
            ).grid(row=4, column=0, sticky=W + E)

# Button Select file py
Button(root, text="Select a file py", command=openfile, width=12, padx=0, pady=8
       ).grid(row=0, column=1, padx=5)

# Button Change folder
Button(root, text="Change Folder", command=change_output, width=12, padx=0, pady=8
       ).grid(row=1, column=1, padx=5)

# Frame Icon file .exe
frame_icon = LabelFrame(root, text="Icon file .exe")
frame_icon.grid(row=2, column=1, rowspan=5, padx=5, pady=0, sticky=N + S + W + E)

# Option menu icon
path_icon = StringVar()
icon_options = ["Default", " None  ", "Option"]
var_icon = StringVar(value=icon_options[0])
OptionMenu(frame_icon, var_icon, *icon_options, command=option_icon
           ).grid(row=1, column=0, sticky=W + E + S + N, padx=2)

# Label image icon
l_icon = Label(frame_icon, text="icon os\n", image=icon_windowed, anchor=CENTER)
l_icon.grid(row=0, column=0, sticky=W + E + S + N, padx=5)

# Button add data
Button(root, text="Add data", width=12, pady=5, command=add_data, anchor=N
       ).grid(row=7, column=1, padx=5, pady=10, sticky=W + E + S + N)

# Frame add data
frame_add_data = LabelFrame(root, text="Data add")
frame_add_data.grid(row=7, column=0, padx=5, sticky=W + E + S + N)

# Label add data
var_add_data = StringVar()
label_add_data = Label(frame_add_data, textvariable=var_add_data, width=30, anchor=W)
label_add_data.grid()

# Button Convert
b_convert = Button(root, text="Convert", state=DISABLED, command=click_convert, padx=20, pady=7)
b_convert.grid(row=8, column=0, columnspan=2, padx=0, pady=10)

# Label State app
converting = StringVar(value="State")
l_state = Label(root, textvariable=converting, fg="blue")
l_state.grid(row=9, column=0, columnspan=2, sticky=W + E)

# Frame Console
frame_console = LabelFrame(root, text="Console", bg="black", padx=0, pady=0, fg="white")
frame_console.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

# Label Console
var_console = StringVar(value="")
Label(frame_console, textvariable=var_console, bg="black", fg="white",
      width=43, height=4, anchor=S + W, justify=LEFT, wraplength=325
      ).grid(padx=5, pady=5)


if __name__ == '__main__':
    root.mainloop()
