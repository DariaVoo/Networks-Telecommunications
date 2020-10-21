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

        menu = Menu(self)
        menu.add_command(label='Upload to server', command=self.load_to_serv)
        self.master.config(menu=menu)

        from FTP_client.frames.StartPage import FTP_MIRROR
        info = "MIRROR: " + str(FTP_MIRROR)
        Label(self, text=info).grid(row=1, column=1)
        Button(self, text="Disconnect",
               command=self.disconnect).grid(row=1, column=2)
        Button(self, text="Upload to server",
               command=self.load_to_serv).grid(row=2, column=1)
        try:
            self.client = Client(FTP_MIRROR)

            self.progress_bar(self.client.connect)
            ft_done("login is successful")

            # self.progress_bar(self.client.connect)
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
        # finally:

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

    def load_to_serv(self):
        """ Загрузить что-то на сервер """
        try:
            file_name: str = filedialog.askopenfilename(initialdir="/home/snorcros", title="Select a File",
                                                   filetypes=(("Text files",
                                                               "*.txt*"),
                                                              ("all files",
                                                               "*.*")))
            if file_name:
                print(file_name)
                progressbar = Progressbar(self, orient='horizontal', length=200, mode='indeterminate')
                progressbar.grid(row=2, column=2)
                progressbar.config(maximum=100, value=0)

                load_thread = threading.Thread(target=self.client.load, args=(file_name,))
                load_thread.start()

                progressbar.start(interval=50)
                while load_thread.is_alive():
                    self.master.update_idletasks()
                    time.sleep(0.05)

                file_name = file_name.split(sep='/')[-1]
                progressbar.stop()
                progressbar.destroy()
                ft_done("File " + file_name + " was load to server")
                self.add_file_to_root(file_name)
        except ConnectionResetError:
            ft_error("Server died :c")
            self.disconnect()
        except Exception as e:
            ft_error(e)

    def progress_bar(self, fun):
        """ TODO: Надо доделать"""
        progressbar = Progressbar(self, orient='horizontal', length=150, mode='indeterminate')
        progressbar.grid(row=2, column=2)
        progressbar.config(maximum=100, value=0)

        save_thread = threading.Thread(target=fun)

        save_thread.start()

        progressbar.start(interval=50)
        while save_thread.is_alive():
            self.master.update_idletasks()
            time.sleep(0.05)

        progressbar.stop()
        progressbar.destroy()

    def save(self, file_name, row):
        """ Скачать что-то с сервера """
        try:
            path: str = filedialog.askdirectory(initialdir="/home/snorcros", title="Select a dir for download", mustexist=1)

            if path:
                progressbar = Progressbar(self, orient='horizontal', length=150, mode='indeterminate')
                progressbar.grid(row=row, column=4)
                progressbar.config(maximum=100, value=0)

                save_thread = threading.Thread(target=self.client.save, args=(file_name, path))
                save_thread.start()

                progressbar.start(interval=50)
                while save_thread.is_alive():
                    self.master.update_idletasks()
                    time.sleep(0.05)

                progressbar.stop()
                progressbar.destroy()
                ft_done("File " + file_name + " was download to " + path)
        except ConnectionResetError:
            ft_error("Server died :c")
            self.disconnect()
        except Exception as e:
            ft_error(e)

    def explore_dir(self, dir_name):
        try:
            self.remove_file_rows_from_root()
            self.dirs = self.client.get_name_dirs(dir_name=dir_name)
            files = self.client.get_name_files()
            self.add_file_rows_to_root(files)
            Button(self, text="Back",
                   command=lambda: self.explore_dir('../')).grid(row=2, column=3)
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
            save_callback_with_name2 = functools.partial(self.explore_dir, file_name)
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
