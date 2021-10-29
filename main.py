import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from modules.resource_path import path
from modules.singleInstance import GetMutex
from modules.subprocess_args import subprocess_args
from interface.input import InFile
from interface.output import OutFile
from interface.options import Options
from interface.add_data import AddData
from interface.convert import Convert
from interface.info import Info
from interface.converting import Converting
from interface.progress_bar import ProgressBar
import os
import threading
import subprocess
import time
import shutil
import sys


class SplashFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        self.master = master
        self.bar = ProgressBar(self)
        self.checking_install = True
        self.getting_version = True
        self.checking_update = True
        self.error = False
        self.pack()

    def check_install(self):
        if subprocess.Popen("pyinstaller --version", **subprocess_args(True)).wait():
            # pyinstaller not install, check pip installed
            if subprocess.Popen("pip --version", **subprocess_args(True)).wait():
                # pip not install, check python installed
                if subprocess.Popen("python --version", **subprocess_args(True)).wait():
                    # python not install
                    mess = "Python not found!"
                else:
                    # python installed and pip not install
                    mess = "PIP not found!"
                messagebox.showerror(title="Error", message="Can't install pyinstaller\n" + mess)
                self.error = True
            else:
                # pip installed, install pyinstaller
                p = subprocess.Popen("pip install pyinstaller", **subprocess_args(True))
                _, errs = p.communicate()
                err = errs.decode()
                if err:
                    messagebox.showerror(title="Error", message="Can't install pyinstaller\n" + err)
                    self.error = True
        self.checking_install = False

    def get_version(self):
        global version
        v = subprocess.Popen("pyinstaller --version", **subprocess_args(True))
        outs, _ = v.communicate()
        version = outs.decode()[:-1]

        self.getting_version = False

    def check_update(self):
        global can_update
        p = subprocess.Popen("pip list --outdated", **subprocess_args(True))
        for outdated in p.stdout:
            if "pyinstaller" in outdated.decode():
                can_update = True
                break
        self.checking_update = False

    def run(self):
        ran = False
        value = 0
        threading.Thread(target=self.check_install).start()
        while not self.error and (value < 100 or self.checking_install or self.getting_version): # or self.checking_update
            time.sleep(0.01)
            if not self.checking_install and not ran:
                threading.Thread(target=self.get_version).start()
                # threading.Thread(target=self.checking_update).start()
                ran = True
            value += 1
            if self.checking_install:
                value = min(value, 49)
            if self.getting_version:
                value = min(value, 99)
            self.bar.set(value)
            self.update_idletasks()
            self.update()
        time.sleep(0.1)
        self.master.destroy()


class SplashScreen(tk.Tk):
    """Splash screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self["bg"] = "#18d1db"
        self.splash = SplashFrame(self)
        self.update_idletasks()
        x = self.winfo_screenwidth() // 2 - self.winfo_width() // 2
        y = self.winfo_screenheight() // 2 - self.winfo_height() * 3 // 5
        self.geometry(f"+{x}+{y}")
        self.overrideredirect(True)
        self.after(1000, self.splash.run)
        self.mainloop()


class MainFrame(tk.Frame):
    """Main GUI and connect all"""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        self.run_animation = tk.BooleanVar(value=True)
        self.name_file = ""
        self.path_in = ""
        self.path_out = ""
        self.path_icon = ""
        self.data = []

        self.infile = InFile(self)
        self.out = OutFile(self)
        windowed = ImageTk.PhotoImage(Image.open(os.path.join(path(), "add", "icon", "windowed.ico")).resize((32, 32)))
        console = ImageTk.PhotoImage(Image.open(os.path.join(path(), "add", "icon", "console.ico")).resize((32, 32)))
        self.option = Options(self, (windowed, console))
        self.add = AddData(self)
        self.convert = Convert(self)
        self.info = Info(self, version)
        self.converting = Converting(self)

        self.infile.set_command(self.on_select)
        self.infile.set_trace(self.on_change_path)
        self.out.set_command(self.on_change)
        self.convert.set_command(self.on_convert)

        self.pack()

    def on_select(self):
        in_path = filedialog.askopenfilename(
            title="Chose a python file", filetypes=(("Python file", ".py .pyw"), ("All file", "*.*")))
        if in_path:
            self.infile.set_path(in_path)
            self.out.set_path(os.path.dirname(in_path))
            tail = os.path.splitext(os.path.basename(in_path))[1]
            if tail == ".pyw":
                self.option.disable_noconsole()
            else:
                self.option.enable_noconsole()
            self.add.add_all(os.path.dirname(in_path))

    def on_change_path(self):
        in_path = self.infile.get_path()
        if os.path.isfile(in_path):
            self.infile.set_path(in_path)
            self.out.set_path(os.path.dirname(in_path))
            tail = os.path.splitext(os.path.basename(in_path))[1]
            if tail == ".pyw":
                self.option.disable_noconsole()
            else:
                self.option.enable_noconsole()
            self.add.add_all(os.path.dirname(in_path))
        else:
            self.add.remove_all()

    def on_change(self):
        out_path = filedialog.askdirectory()
        if out_path:
            self.out.set_path(out_path)

    def check_ready(self):
        if not self.infile.get_path():
            return "The path of python file must not be empty!"
        if not self.out.get_path():
            return "The path of folder put your app must not ne empty!"
        return "ok"

    def on_convert(self):
        mess = self.check_ready()
        if mess != "ok":
            messagebox.showwarning(title="Convert py to exe", message=mess)
            return
        self.name_file = self.infile.get_name()
        self.path_in = os.path.normpath(self.infile.get_path())
        self.path_out = os.path.normpath(self.out.get_path())
        icon = self.option.get_path()
        self.path_icon = os.path.normpath(icon) if icon else ""
        self.data = self.add.get_add()
        self.convert.disable()
        self.convert.set_text("Converting...", color="#191cf7")
        threading.Thread(target=self.run).start()
        self.run_animation.set(value=True)
        self.converting.run_animation(self.run_animation)

    def run(self):
        command = self.create_command()
        print(command)
        p = subprocess.Popen(command, **subprocess_args(True))
        err = ""
        for e in p.stderr:
            err = e.decode()[:-1]
        if p.wait():
            self.convert.set_text("Convert Failed", color="#9e0000")
            self.run_animation.set(value=False)
            self.converting.convert_fail()
            messagebox.showerror(title="Convert py to exe", message="Convert failed" + err)
        else:
            self.convert.set_text("Successfully", color="#008f13")
            self.run_animation.set(value=False)
            self.converting.convert_suc()
            ok = messagebox.askyesno(title="Convert py to exe",
                                     message="Convert Successfully\nDo you want to delete .spec file")
            if ok:
                os.unlink(os.path.join(os.path.dirname(self.path_in), self.name_file + ".spec"))
        shutil.rmtree(os.path.join(path(), "build", self.name_file))
        self.convert.enable()

    def create_command(self):
        command = f'pyinstaller --clean --specpath "{os.path.dirname(self.path_in)}" ' \
                  f'--distpath "{self.path_out}" --workpath "{os.path.join(path(), "build")}" ' \
                  f'--name "{self.name_file}" '
        if self.path_icon:
            command += f'--icon="{self.path_icon}" '
        for data in self.data:
            path_data = os.path.dirname(self.path_in) + "/" + data
            if os.path.isfile(path_data):
                command += f'--add-data="{path_data};." '
            else:
                command += f'--add-data="{path_data};{data}" '
        if self.option.onfile():
            command += "--onefile "
        if self.option.noconsole():
            command += "--noconsole "
        if self.option.admin():
            command += "--uac-admin "
        command += f'"{self.infile.get_path()}"'
        return command


class MainScreen(tk.Tk):
    """main screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("Convert py to exe")
        self["bg"] = "#71c9ce"
        icon = os.path.join(path(), "add", "icon", "icon.ico")
        self.iconbitmap(icon)
        MainFrame(self)
        self.update_idletasks()
        x = self.winfo_screenwidth() // 2 - self.winfo_width() // 2
        y = self.winfo_screenheight() // 2 - self.winfo_height() * 3 // 5
        self.geometry(f"+{x}+{y}")
        self.minsize(self.winfo_width(), self.winfo_height())
        self.mainloop()


if __name__ == '__main__':
    app = GetMutex()
    if app.is_running():
        sys.exit(0)

    version = ""
    can_update = False
    SplashScreen()
    if version:
        MainScreen()
