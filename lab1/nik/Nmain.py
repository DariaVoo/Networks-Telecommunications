import tkinter.ttk
import tkinter
import tkinter.filedialog
import functools

from nik.sc import Client


def cb(event):
    print('fuck')

class ClientGui:
    def __init__(self):
        self.client = Client()

        self.root = tkinter.Tk()
        self.address_label = tkinter.ttk.Label(self.root, text='Address')
        self.address_label.grid(row=1, column=1)

        self.port_label = tkinter.ttk.Label(self.root, text='Port')
        self.port_label.grid(row=1, column=2)

        self.address_entry = tkinter.ttk.Entry(self.root)
        self.address_entry.grid(row=2, column=1, padx=5, pady=5)

        self.port_entry = tkinter.ttk.Entry(self.root)
        self.port_entry.grid(row=2, column=2, padx=5, pady=5)

        self.connect_btn = tkinter.ttk.Button(self.root, text='Connect')
        self.connect_btn.grid(row=3, column=2)
        self.connect_btn.bind('<Button-1>', self.connect_callback)
        self.connect_btn.bind('<Return>', self.connect_callback)

        self.connection_label = tkinter.ttk.Label(self.root, text='Disonnected')
        self.connection_label.grid(row=3, column=1)

        self.file_widgets = []
    
        self.current_row = 3

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        if tb is None:
            # i'm lazy
            if self.client.is_active():
                self.client.close()

    def add_filedialog_and_disconnect_btn(self):
        # disconnect_btn
        disconnect_btn = tkinter.ttk.Button(self.root, text='Disconnect')
        disconnect_btn.grid(row=self.current_row, column=2)
        disconnect_btn.bind('<Button-1>', self.disconnect_callback)
        
        # filedialog
        file_dialog_btn = tkinter.ttk.Button(self.root, text='Load to server')
        file_dialog_btn.grid(row=self.current_row, column=3)
        file_dialog_btn.bind('<Button-1>', self.load_callback)

        self.file_widgets.append(disconnect_btn)
        self.file_widgets.append(file_dialog_btn)
        self.current_row += 1 

    def add_file_rows_to_root(self, file_names: list):
        for file_name in file_names:
            file_name_label = tkinter.ttk.Label(self.root, text=file_name)
            file_download_button = tkinter.ttk.Button(self.root, text='Download')
            save_callback_with_name = functools.partial(self.save_callback, file_name)
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

    def connect_callback(self, event):
        connection_address = self.address_entry.get()
        connection_port = self.port_entry.get()
        
        # if not None or '' 
        if connection_address is not None and connection_port is not None and connection_address != '' and connection_port != '':
            try:
                self.client.connect(connection_address, int(connection_port))
                file_names = self.client.get_file_names()
                self.add_filedialog_and_disconnect_btn()
                self.add_file_rows_to_root(file_names)

                event.widget.grid_remove()
                self.connection_label['text'] = 'Connected'
            except:
                pass

    def disconnect_callback(self, event):
        self.client.close()
        self.remove_file_rows_from_root()
        self.connection_label['text'] = 'Disconnected'
        # remove the disctonnect_btn

        # event.widget.grid_remove()
        # put the connect_btn back on the grid
        self.connect_btn.grid()

    def load_callback(self, event):
        file_name = tkinter.filedialog.askopenfilename()
        if file_name != '':
            self.client.load_file(file_name)

    def save_callback(self, file_name, event):
        self.client.save_file(file_name)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    with ClientGui() as gui:
        gui.run()
    
    

