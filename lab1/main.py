from frames.TCPApp import TCPApp
from client import client
from threading import Thread
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog


if __name__ == "__main__":
    # print(TCP_IP, TCP_PORT)
    app = TCPApp()
    app.mainloop()


    # thread1 = Thread(target=server, args=(TCP_IP, TCP_PORT))
    # thread2 = Thread(target=client, args=(TCP_IP, TCP_PORT, 'load', 'a.txt'))
    # # thread2 = Thread(target=client, args=(TCP_IP, TCP_PORT, 'download', '1'))
    #
    # thread1.start()
    # thread2.start()
    # thread1.join()
    # thread2.join()
