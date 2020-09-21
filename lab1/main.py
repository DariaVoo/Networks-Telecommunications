from server import server
from client import client
from threading import Thread
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog


# print('Введите IP сервера')
# TCP_IP = str(input())
# print('Введите PORT сервера')
# TCP_PORT = int(input())

def ft_error(msg: str):
    messagebox.showerror("Error", msg)


def get_params():
    try:
        TCP_IP = str(e1.get())
        if re.fullmatch(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', TCP_IP) is None:
            raise Exception("Invalid IP! IP must be like 127.0.0.1!")
        TCP_PORT = int(e2.get())
        print(TCP_IP, TCP_PORT)
        return TCP_IP, TCP_PORT
    except ValueError:
        ft_error("Invalid port! Port must be a number!")
    except Exception as e:
        ft_error(e)


def browse_files(label_file_explorer):
    """ Function for opening the file explorer window """
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      "*.*")))

    # Change label contents
    label_file_explorer.configure(text="File Opened: " + filename)


if __name__ == "__main__":
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5052
    # print(TCP_IP, TCP_PORT)

    master = Tk()
    master.title("Lab1 - TCP")
    master.geometry('360x260')

    # adding menu bar in root window
    # new item in menu bar labelled as 'New'
    # adding more items in the menu bar
    menu = Menu(master)
    item = Menu(menu)
    item.add_command(label='New')
    menu.add_cascade(label='File', menu=item)
    master.config(menu=menu)

    Label(master, text="IP").grid(row=0)
    Label(master, text="Port").grid(row=1)

    e1 = Entry(master, exportselection=0)
    e2 = Entry(master, exportselection=0)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    w = Button(master, text="Run", command=get_params).grid(column=1)
    mainloop()

    # thread1 = Thread(target=server, args=(TCP_IP, TCP_PORT))
    # thread2 = Thread(target=client, args=(TCP_IP, TCP_PORT, 'load', 'a.txt'))
    # # thread2 = Thread(target=client, args=(TCP_IP, TCP_PORT, 'download', '1'))
    #
    # thread1.start()
    # thread2.start()
    # thread1.join()
    # thread2.join()
