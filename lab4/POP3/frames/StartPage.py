from tkinter import Frame, Label, Entry, Button

from POP3.frames.PageOne import PageOne
from SMTP.utils.ft_error import ft_error

POP3_ADDRESS: str = "dariavvoroncova@gmail.com"


def get_params(e1, master):
    try:
        global POP3_ADDRESS
        POP3_ADDRESS = str(e1.get())
        print(POP3_ADDRESS)
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
        Label(self, text="Email Address").grid(row=0)

        e1 = Entry(self, exportselection=0)
        e1.grid(row=0, column=1)
        w = Button(self, text="Run", command=lambda: get_params(e1, master)).grid(column=1)
