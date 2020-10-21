from tkinter import Frame, Label, Entry, Button

from FTP_client.frames.PageOne import PageOne
from FTP_client.utils.ft_error import ft_error

FTP_MIRROR: str = 'ftp.debian.org'


def get_params(e1, master):
    try:
        global FTP_MIRROR
        FTP_MIRROR = str(e1.get())
        print(FTP_MIRROR)
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
        Label(self, text="Mirror").grid(row=0)

        e1 = Entry(self, exportselection=0)
        e1.grid(row=0, column=1)
        w = Button(self, text="Run", command=lambda: get_params(e1, master)).grid(column=1)
