from tkinter import filedialog, Frame, Label, Button

from client import Client
from utils.ft_error import ft_error


def browse_files():
    """ Function for opening the file explorer window """
    filename = filedialog.askopenfilename(initialdir="/home/snorcros",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      "*.*")))
    print(filename)


class PageOne(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self, bg='blue')
        Label(self, text="Page one", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        from frames.StartPage import TCP_IP
        from frames.StartPage import TCP_PORT
        print(TCP_IP, TCP_PORT)

        # try:
        cli = Client(TCP_IP, TCP_PORT)
        files = cli.get_name_files()
        # except Exception as e:
        #     ft_error(e)
        # finally:
        cli.close()

        from frames.StartPage import StartPage
        Button(self, text="Go back to start page",
               command=lambda: master.switch_frame(StartPage)).pack()



