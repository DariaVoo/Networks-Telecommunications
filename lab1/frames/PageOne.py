import functools
from tkinter import filedialog, Frame, Label, Button, Menu
from tkinter.ttk import Progressbar

from client import Client
from utils.ft_done import ft_done
from utils.ft_error import ft_error


class PageOne(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self)
        self.master = master
        self.file_widgets = []
        self.current_row = 3

        # adding menu bar in master window
        menu = Menu(self)
        menu.add_command(label='Upload to server', command=self.load_to_serv)
        self.master.config(menu=menu)

        from frames.StartPage import TCP_IP
        from frames.StartPage import TCP_PORT
        info = "IP: " + str(TCP_IP) + "\tPORT: " + str(TCP_PORT)
        Label(self, text=info).grid(row=1, column=1)
        Button(self, text="Disconnect",
               command=self.disconnect).grid(row=1, column=2)
        Button(self, text="Upload to server",
               command=self.load_to_serv).grid(row=2, column=1)
        # try:
        self.client = Client(TCP_IP, TCP_PORT)
        files = self.client.get_name_files()
        self.add_file_rows_to_root(files)

        # except Exception as e:
        #     ft_error(e)
        # finally:

    def disconnect(self):
        self.client.close()
        self.remove_file_rows_from_root()
        from frames.StartPage import StartPage
        self.master.switch_frame(StartPage)

    def load_to_serv(self):
        """ Загрузить что-то на сервер """
        file_name = filedialog.askopenfilename(initialdir="/home/snorcros", title="Select a File",
                                               filetypes=(("Text files",
                                                           "*.txt*"),
                                                          ("all files",
                                                           "*.*")))
        if file_name != '':
            self.client.load(file_name)
            file_name = file_name.split(sep='/')[-1]
            ft_done("File " + file_name + " was load to server")
            self.add_file_to_root(file_name)

    def run_bar(self, progressbar: Progressbar):
        currentValue = 0
        divisions = 10
        for i in range(divisions):
            currentValue = currentValue + 10
            # progressbar.after(500, progress(currentValue))
            # progressbar.update()  # Force an update of the GUI
            progressbar.step()

    def save(self, file_name, row, event):
        """ Скачать что-то с сервера """
        progressbar = Progressbar(self, orient='horizontal', length=150, mode='indeterminate')
        progressbar.grid(row=row, column=4)
        progressbar.config(maximum=100, value=0)
        progressbar.start(interval=50)

        # self.run_bar(progressbar)
        path = filedialog.askdirectory(initialdir="/home/snorcros", title="Select a dir for download", mustexist=1)
        self.client.save(file_name, path)
        ft_done("File " + file_name + " was download to " + path)

        progressbar.stop()

    def add_file_rows_to_root(self, file_names: list):
        for file_name in file_names:
            self.add_file_to_root(file_name)

    def add_file_to_root(self, file_name: list):
        file_name_label = Label(self, text=file_name)
        file_download_button = Button(self, text='Download')
        save_callback_with_name = functools.partial(self.save, file_name, self.current_row)
        file_download_button.bind('<Button-1>', save_callback_with_name)

        self.file_widgets.append(file_download_button)

        # bind with partial
        file_name_label.grid(row=self.current_row, column=1)
        file_download_button.grid(row=self.current_row, column=2)
        self.file_widgets.append(file_name_label)

        self.current_row += 1

    def remove_file_rows_from_root(self):
        for widget in self.file_widgets:
            widget.grid_remove()
        self.file_widgets.clear()
        self.current_row = 3
        print(self.current_row)

    def __exit__(self, type, value, tb):
        if tb is None:
            if self.client.is_active():
                self.client.close()
