import re
from tkinter import Frame, Menu, Label, Entry, Button

from frames.PageOne import PageOne
from utils.ft_error import ft_error

ADR_SRC: str = '127.0.0.1'
ADR_DEST: str = '127.0.0.1'


def get_params(e1, e2, master):
    try:
        global ADR_SRC, ADR_DEST
        ADR_SRC = str(e1.get())
        if re.fullmatch(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', ADR_SRC) is None:
            raise Exception("Invalid Sender Address! Address must be like 127.0.0.1!")
        ADR_DEST = str(e2.get())
        if re.fullmatch(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', ADR_DEST) is None:
            raise Exception("Invalid Destination Address! Address must be like 127.0.0.1!")
        print(ADR_SRC, ADR_DEST)
        master.switch_frame(PageOne)
    except ConnectionRefusedError:
        ft_error("Server is not available :c")
    except ValueError:
        ft_error("Invalid port! Port must be a number!")
    except Exception as e:
        ft_error(e)


class StartPage(Frame):
    def __init__(self, master, async_loop):
        Frame.__init__(self, master)
        self.async_loop = async_loop
        Label(self, text="Sender Address").grid(row=0)
        Label(self, text="Destination Address").grid(row=1)

        e1 = Entry(self, exportselection=0)
        e2 = Entry(self, exportselection=0)
        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        w = Button(self, text="Run", command=lambda: get_params(e1, e2, master)).grid(column=1)
