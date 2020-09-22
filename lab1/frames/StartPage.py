import re
from tkinter import Frame, Menu, Label, Entry, Button

from frames.PageOne import PageOne
from utils.ft_error import ft_error

TCP_IP: str = '127.0.0.1'
TCP_PORT: int = 5052


def get_params(e1, e2, master):
    try:
        global TCP_IP, TCP_PORT
        TCP_IP = str(e1.get())
        if re.fullmatch(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', TCP_IP) is None:
            raise Exception("Invalid IP! IP must be like 127.0.0.1!")
        TCP_PORT = int(e2.get())
        print(TCP_IP, TCP_PORT)
        master.switch_frame(PageOne)
    except ValueError:
        ft_error("Invalid port! Port must be a number!")
    except Exception as e:
        ft_error(e)


class StartPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="IP").grid(row=0)
        Label(self, text="Port").grid(row=1)

        e1 = Entry(self, exportselection=0)
        e2 = Entry(self, exportselection=0)
        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        w = Button(self, text="Run", command=lambda: get_params(e1, e2, master)).grid(column=1)
