from frames.TCPApp import TCPApp
from client import client
from threading import Thread
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog


if __name__ == "__main__":
    # print(TCP_IP, TCP_PORT)
    # app = TCPApp()
    # app.mainloop()

    tcp_ip: str = '127.0.0.1'
    tcp_port: int = 5060
    # thread1 = Thread(target=server, args=(TCP_IP, TCP_PORT))
    thread2 = Thread(target=client, args=(tcp_ip, tcp_port, 'load', 'b.txt'))
    # thread2 = Thread(target=client, args=(TCP_IP, TCP_PORT, 'download', '1'))
    #
    # thread1.start()
    thread2.start()
    # thread1.join()
    thread2.join()
