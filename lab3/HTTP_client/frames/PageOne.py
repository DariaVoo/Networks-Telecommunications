import functools
import threading
import time
import tkinter
from tkinter import filedialog, Frame, Label, Button, Menu, messagebox, Text, INSERT, LEFT
from tkinter.ttk import Progressbar

from pip._vendor import requests

from FTP_client.utils.ft_done import ft_done
from FTP_client.utils.ft_error import ft_error


class PageOne(Frame):
    def __init__(self, master, async_loop):
        Frame.__init__(self, master)
        self.async_loop = async_loop
        Frame.configure(self)
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.current_row = 3
        self.html = ''
        self.text_frame = None

        from HTTP_client.frames.StartPage import ADDRESS
        info = "Address " + str(ADDRESS)
        Label(self, text=info).grid(row=1, column=1)
        Button(self, text="Disconnect",
               command=self.disconnect).grid(row=1, column=2)

        try:
            if ADDRESS[:5] != 'http':
                r = requests.get('https://' + ADDRESS)
            self.html = str(r.text)

            text = Text()
            text.insert(INSERT, self.html)
            text.configure(state='disabled')
            text.grid(row=2, column=1)
            self.text_frame = text

            # print(r.text[:200])
            # Label(self, text=self.html).grid(row=2, column=1)
            # text_frame.insert(INSERT, "Hello.....")
            # self.text_frame.insert(tkinter.END, self.html)
        except Exception as e:
            ft_error(e)

    def disconnect(self):
        from HTTP_client.frames.StartPage import StartPage
        if self.text_frame is not None:
            self.text_frame.destroy()
        self.master.switch_frame(StartPage)

    def progress_bar(self, fun):
        progressbar = Progressbar(self, orient='horizontal', length=150, mode='indeterminate')
        progressbar.grid(row=2, column=2)
        progressbar.config(maximum=100, value=0)

        save_thread = threading.Thread(target=fun)

        save_thread.start()

        progressbar.start(interval=50)
        while save_thread.is_alive():
            self.master.update_idletasks()
            time.sleep(0.05)

        progressbar.stop()
        progressbar.destroy()

    def on_closing(self):
        """" При закрытии приложения отключаемся от сервера """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()
