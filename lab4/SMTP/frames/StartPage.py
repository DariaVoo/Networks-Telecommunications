import functools
import threading
import time
from tkinter import Frame, Label, Entry, Button, Text, END
from tkinter.ttk import Progressbar

from SMTP.send_msg import send_msg
from SMTP.utils.ft_done import ft_done
from SMTP.utils.ft_error import ft_error


class StartPage(Frame):
    def __init__(self, master, async_loop):
        Frame.__init__(self, master)
        self.async_loop = async_loop
        Frame.configure(self)
        self.master = master

        Label(self, text="To").grid(row=0)
        e1 = Entry(self, exportselection=0)
        e1.grid(row=0, column=1)

        Label(self, text="Subject").grid(row=1)
        subject = Text(self, height=1)
        subject.grid(row=1, column=1)

        Label(self, text="Message").grid(row=2)
        msg = Text(self)
        msg.grid(row=2, column=1)

        send_callback = functools.partial(self.send, e1, subject, msg)
        send_button = Button(self, text='Send', command=send_callback)
        send_button.grid(column=1)

    def send(self, e1, subj, msg):
        try:
            to = str(e1.get())
            subject = subj.get("1.0", END)
            message = msg.get("1.0", END)
            print(subject, message)
            to = "dariavvoroncova@gmail.com"

            progressbar = Progressbar(self, orient='horizontal', length=200, mode='indeterminate')
            progressbar.grid(column=1)
            progressbar.config(maximum=100, value=0)

            load_thread = threading.Thread(target=send_msg, args=(to, subject, message))
            load_thread.start()

            progressbar.start(interval=10)
            while load_thread.is_alive():   # NEED fix
                self.master.update_idletasks()
                time.sleep(0.05)

            progressbar.stop()
            progressbar.destroy()
            ft_done(f"successfully sent email to {to}")

        except Exception as e:
            ft_error(e)
