import asyncio
import functools
import threading
from tkinter import filedialog, Frame, Label, Button, Menu, messagebox
from tkinter.ttk import Progressbar

from client import Client
from main import do_tasks
from utils.ft_done import ft_done
from utils.ft_error import ft_error


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

        from frames.StartPage import TCP_IP
        from frames.StartPage import TCP_PORT
        info = "IP: " + str(TCP_IP) + "\tPORT: " + str(TCP_PORT)
        Label(self, text=info).grid(row=1, column=1)
        Button(self, text="Disconnect",
               command=self.disconnect).grid(row=1, column=2)
        Button(self, text="Upload to server",
               command=self.load_to_serv).grid(row=2, column=1)
        try:
            self.client = Client(TCP_IP, TCP_PORT)
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
        from frames.StartPage import StartPage
        self.master.switch_frame(StartPage)

    # async def l(self, file_name):
    #     await asyncio.wait(self.client.load(file_name))

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
                progressbar.start(interval=50)

                load_thread = threading.Thread(target=self.client.load, args=(file_name,))
                load_thread.start()
                # self.client.load(file_name)
                while load_thread.is_alive():
                    progressbar.step()

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

    def save(self, file_name, row):
        """ Скачать что-то с сервера """
        try:
            path: str = filedialog.askdirectory(initialdir="/home/snorcros", title="Select a dir for download", mustexist=1)

            if path:
                progressbar = Progressbar(self, orient='horizontal', length=150, mode='indeterminate')
                progressbar.grid(row=row, column=4)
                progressbar.config(maximum=100, value=0)
                progressbar.start(interval=50)

                self.client.save(file_name, path)

                progressbar.stop()
                progressbar.destroy()
                ft_done("File " + file_name + " was download to " + path)
        except ConnectionResetError:
            ft_error("Server died :c")
            self.disconnect()
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
            if self.client.active:
                self.client.close()
            self.master.destroy()
