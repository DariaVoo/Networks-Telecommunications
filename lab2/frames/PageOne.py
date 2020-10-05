import functools
import threading
import time
from tkinter import filedialog, Frame, Label, Button, Menu, messagebox
from tkinter.ttk import Progressbar

from do_ip_package import do_ip_package
from utils.ft_error import ft_error


class PageOne(Frame):
    def __init__(self, master, async_loop):
        Frame.__init__(self, master)
        self.async_loop = async_loop
        Frame.configure(self)
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.file_widgets = []
        self.current_row = 3
        self.client = None

        menu = Menu(self)
        # menu.add_command(label='Upload to server', command=self.load_to_serv)
        self.master.config(menu=menu)

        from frames.StartPage import ADR_SRC
        from frames.StartPage import ADR_DEST
        info = "Sender Address: " + str(ADR_SRC) + "\tDestination Address: " + str(ADR_DEST)
        Label(self, text=info).grid(row=1, column=1)

        do_ip_callback = functools.partial(do_ip_package, "First_fil", ADR_SRC, ADR_DEST)
        Button(self, text="Do IP Package", command=do_ip_callback).grid(row=1, column=2)

        try:
            a = 0
            # self.client = Client(ADR_SRC, ADR_DEST)
            # files = self.client.get_name_files()
        except Exception as e:
            ft_error(e)

    def on_closing(self):
        """" При закрытии приложения отключаемся от сервера """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()
