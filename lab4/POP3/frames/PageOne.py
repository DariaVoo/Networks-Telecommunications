import functools
import threading
import time
from tkinter import filedialog, Frame, Label, Button, Menu, messagebox
from tkinter.ttk import Progressbar

from POP3.client import Client
from SMTP.utils.ft_done import ft_done
from SMTP.utils.ft_error import ft_error


class PageOne(Frame):
    def __init__(self, master, async_loop):
        Frame.__init__(self, master)
        self.async_loop = async_loop
        Frame.configure(self)
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.msg_widgets = []
        self.current_row = 3
        self.client = None
        self.btn_back = None
        self.msgs: list = None
        self.labels = []

        from POP3.frames.StartPage import POP3_ADDRESS
        info = "Email Address: " + str(POP3_ADDRESS)
        self.info_label = Label(self, text=info).grid(row=1, column=2)
        self.btn_disconnect = Button(self, text="Log Out",
               command=self.disconnect).grid(row=1, column=1)
        self.add_label("Date", 2, 1)
        self.add_label("From", 2, 2)
        self.add_label("To", 2, 3)
        self.add_label("Subject", 2, 4)

        self.client = Client(POP3_ADDRESS)

        t1 = threading.Thread(target=self.client.connect)
        t1.start()
        t_progr = threading.Thread(target=self.progress, args=(3, t1)).start()
        ft_done("login is successful")

        t2 = threading.Thread(target=self.connect)
        t2.start()
        t_progr = threading.Thread(target=self.progress, args=(1, t2)).start()

    def add_label(self, text, row, column):
        label = Label(self, text=text)
        label.configure(font=("Times New Roman", 12, "bold"))
        label.grid(row=row, column=column)
        self.labels.append(label)

    def connect(self):
        try:

            self.msgs = self.client.get_msgs()
            self.add_msg_rows_to_root(self.msgs)

        except ConnectionRefusedError:
            raise ConnectionRefusedError
        except ConnectionResetError:
            ft_error("Server died :c")
            self.disconnect()
        except Exception as e:
            ft_error(e)

    def get_email_content(self, msg, current_row):
        email_date, email_from, email_to, email_subject, email_content = msg
        current_msg = []

        self.remove_msg_rows_from_root()
        self.remove_widgets(self.labels)

        self.add_label("Date", 2, 1)
        self.add_label("From", 3, 1)
        self.add_label("To", 4, 1)
        self.add_label("Subject", 5, 1)
        self.add_label("Content", 6, 1)

        label_date = Label(self, text=email_date)
        label_from = Label(self, text=email_from)
        label_to = Label(self, text=email_to)
        label_subj = Label(self, text=email_subject)
        label_content = Label(self, text=email_content)

        current_msg.append(label_date)
        current_msg.append(label_from)
        current_msg.append(label_to)
        current_msg.append(label_subj)
        current_msg.append(label_content)

        row = 2
        for label in current_msg:
            label.grid(row=row, column=2)
            row += 1

        back_callback = functools.partial(self.back, current_msg)
        button_back = Button(self, text="Back", command=back_callback)
        button_back.grid(row=1, column=3)
        self.btn_back = button_back

    def back(self, widgets):
        self.remove_widgets(widgets)
        self.remove_widgets(self.labels)

        self.add_label("Date", 2, 1)
        self.add_label("From", 2, 2)
        self.add_label("To", 2, 3)
        self.add_label("Subject", 2, 4)

        self.add_msg_rows_to_root(self.msgs)
        self.btn_back.grid_remove()

    def remove_widgets(self, widgets):
        for widget in widgets:
            widget.grid_remove()

    def add_msg_to_root(self, msg: tuple):
        email_date, email_from, email_to, email_subject, email_content = msg

        label_date = Label(self, text=email_date)
        label_from = Label(self, text=email_from)
        label_to = Label(self, text=email_to)
        label_subj = Label(self, text=email_subject)

        save_callback_with_name = functools.partial(self.get_email_content, msg, self.current_row)
        button_get_content = Button(self, text='Read msg', command=save_callback_with_name)
        self.msg_widgets.append(button_get_content)

        # grid
        label_date.grid(row=self.current_row, column=1)
        label_from.grid(row=self.current_row, column=2)
        label_to.grid(row=self.current_row, column=3)
        label_subj.grid(row=self.current_row, column=4)
        button_get_content.grid(row=self.current_row, column=5)

        self.msg_widgets.append(label_date)
        self.msg_widgets.append(label_from)
        self.msg_widgets.append(label_to)
        self.msg_widgets.append(label_subj)

        self.current_row += 1

    def add_msg_rows_to_root(self, msgs: list):
        for message in msgs:
            self.add_msg_to_root(message)

    def remove_msg_rows_from_root(self):
        self.remove_widgets(self.msg_widgets)
        self.msg_widgets.clear()
        self.current_row = 3

    def progress(self, row, thread):
        progressbar = Progressbar(self, orient='horizontal', length=150, mode='indeterminate')
        progressbar.grid(row=row, column=4)
        progressbar.config(maximum=100, value=0)

        progressbar.start()
        while thread.is_alive():
            self.master.update_idletasks()
            time.sleep(0.05)
        progressbar.stop()
        progressbar.destroy()

    def disconnect(self):
        if self.client:
            try:
                self.client.close()
            except Exception as e:
                print(e)
            finally:
                self.remove_msg_rows_from_root()

        from POP3.frames.StartPage import StartPage
        self.master.switch_frame(StartPage)

    def on_closing(self):
        """" При закрытии приложения отключаемся от сервера """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if self.client and self.client.active:
                self.client.close()
            self.master.destroy()
