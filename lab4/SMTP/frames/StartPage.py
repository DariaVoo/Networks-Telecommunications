import threading
from datetime import time
from tkinter import Frame, Label, Entry, Button, Text, END
from tkinter.ttk import Progressbar

from SMTP.send_msg import send_msg
from SMTP.utils.ft_error import ft_error


def get_params(e1, subj, msg, master):
    try:
        to = str(e1.get())
        subject = subj.get("1.0", END)
        message = msg.get("1.0", END)
        print(subject, message)

        progressbar = Progressbar(master, orient='horizontal', length=200, mode='indeterminate')
        progressbar.grid(column=1)
        progressbar.config(maximum=100, value=0)

        load_thread = threading.Thread(target=send_msg, args=(to, subject, message))
        load_thread.start()

        progressbar.start(interval=50)
        while load_thread.is_alive():
            master.update_idletasks()
            time.sleep(0.05)

        progressbar.stop()
        progressbar.destroy() # NEED fix

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
        Label(self, text="To").grid(row=0)
        e1 = Entry(self, exportselection=0)
        e1.grid(row=0, column=1)

        Label(self, text="Subject").grid(row=1)
        subject = Text(self, height=1)
        subject.grid(row=1, column=1)

        Label(self, text="Message").grid(row=2)
        msg = Text(self)
        msg.grid(row=2, column=1)

        w = Button(self, text="Send", command=lambda: get_params(e1, subject, msg, master)).grid(column=1)
