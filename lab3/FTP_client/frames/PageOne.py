import functools
import threading
import time
from tkinter import filedialog, Frame, Label, Button, Menu, messagebox
from tkinter.ttk import Progressbar

from FTP_client.client import Client
from FTP_client.utils.ft_done import ft_done
from FTP_client.utils.ft_error import ft_error


class PageOne(Frame):
    def __init__(self, master, async_loop):
        Frame.__init__(self, master)
        self.async_loop = async_loop
        Frame.configure(self)
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.file_widgets = []
        self.current_row = 3
        self.client = None

        from FTP_client.frames.StartPage import FTP_MIRROR
        info = "MIRROR: " + str(FTP_MIRROR)
        self.info_label = Label(self, text=info).grid(row=1, column=1)
        self.btn_disconnect = Button(self, text="Disconnect",
               command=self.disconnect).grid(row=1, column=2)

        from FTP_client.frames.StartPage import FTP_MIRROR
        self.client = Client(FTP_MIRROR)

        t1 = threading.Thread(target=self.client.connect)
        t1.start()
        t_progr = threading.Thread(target=self.progress, args=(3, t1)).start()
        ft_done("login is successful")

        t2 = threading.Thread(target=self.connect)
        t2.start()
        t_progr = threading.Thread(target=self.progress, args=(1, t2)).start()

    def connect(self):
        try:
            self.dirs = self.client.get_name_dirs()
            files = self.client.get_name_files()
            self.add_file_rows_to_root(files)

        except ConnectionRefusedError:
            raise ConnectionRefusedError
        except ConnectionResetError:
            ft_error("Server died :c")
            self.disconnect()
        except Exception as e:
            ft_error(e)

    def disconnect(self):
        if self.client:
            try:
                self.client.close()
            except Exception as e:
                print(e)
            finally:
                self.remove_file_rows_from_root()
        from FTP_client.frames.StartPage import StartPage
        self.master.switch_frame(StartPage)

    def save(self, file_name, row):
        """ Скачать что-то с сервера """
        try:
            path: str = filedialog.askdirectory(initialdir="/home/snorcros", title="Select a dir for download", mustexist=1)

            if path:
                t1 = threading.Thread(target=self.client.save, args=(file_name, path))
                t1.start()
                t_progr = threading.Thread(target=self.progress, args=(row, t1)).start()
                ft_done("File " + file_name + " was download to " + path)
        except ConnectionResetError:
            ft_error("Server died :c")
            self.disconnect()
        except Exception as e:
            ft_error(e)

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

    def explore(self, dir_name):
        self.dirs = self.client.get_name_dirs(dir_name=dir_name)
        files = self.client.get_name_files()

        self.remove_file_rows_from_root()
        self.add_file_rows_to_root(files)
        Button(self, text="Back",
               command=lambda: self.explore_dir('../', 2)).grid(row=2, column=3)

    def explore_dir(self, dir_name, current_row):
        try:
            t1 = threading.Thread(target=self.explore, args=(dir_name, ))
            t1.start()
            t2 = threading.Thread(target=self.progress, args=(current_row, t1)).start()

        except Exception as e:
            ft_error(e)

    def add_file_rows_to_root(self, file_names: list):
        for file_name in file_names:
            self.add_file_to_root(file_name)

    def add_file_to_root(self, file_name: list):
        file_name_label = Label(self, text=file_name)

        save_callback_with_name = functools.partial(self.save, file_name, self.current_row)
        file_download_button = Button(self, text='Download', command=save_callback_with_name)
        self.file_widgets.append(file_download_button)

        # grid
        file_name_label.grid(row=self.current_row, column=1)
        file_download_button.grid(row=self.current_row, column=2)

        if file_name in self.dirs or file_name.split('/')[-1] in self.dirs:
            save_callback_with_name2 = functools.partial(self.explore_dir, file_name, self.current_row)
            explore_dir_button = Button(self, text='Explore Dir', command=save_callback_with_name2)
            self.file_widgets.append(explore_dir_button)
            explore_dir_button.grid(row=self.current_row, column=3)

        self.file_widgets.append(file_name_label)

        self.current_row += 1

    def remove_file_rows_from_root(self):
        for widget in self.file_widgets:
            widget.grid_remove()
        self.file_widgets.clear()
        self.current_row = 3

    def on_closing(self):
        """" При закрытии приложения отключаемся от сервера """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if self.client and self.client.active:
                self.client.close()
            self.master.destroy()
