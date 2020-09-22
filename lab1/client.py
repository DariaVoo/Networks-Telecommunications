import socket
from tkinter.ttk import Progressbar

from server import load_file
from utils.ft_done import ft_done


class Client:
    def __init__(self, ip: int, port: int):
        self.TCP_PORT = port
        self.TCP_IP = ip
        self.BUFFER_SIZE = 1024
        self.DIR_FILES = 'client/'
        self.active = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.socket.connect((self.TCP_IP, self.TCP_PORT))
        self.active = True

    def load(self, file_name: str):  # загрузить на сервак
        """ Загрузка данных на сервер """
        self.socket.send((0).to_bytes(2, 'big'))
        print("want to load", file_name)
        self.socket.send((file_name + '\0').encode('utf-8'))
        f = open(file_name, 'rb')
        self.socket.send(f.read())

    def save(self, file_name: str, path: str):  # скачать с сервака
        """ Скачивание данных с сервера """
        self.socket.send((1).to_bytes(2, 'big'))
        self.socket.send(file_name.encode('utf-8'))
        data = self.get_data()
        load_file(self.DIR_FILES + file_name, data.decode('utf-8'))
        print("File was downloaded")

    def get_data(self):
        data = self.socket.recv(self.BUFFER_SIZE)
        tmp = 0
        while tmp:  # Могут быть большие файлы
            data += tmp
            tmp = self.socket.recv(self.BUFFER_SIZE)
        return data

    def get_name_files(self):
        self.socket.send((2).to_bytes(2, 'big'))
        data = self.get_data().decode('utf-8')
        data = data.split()
        print("Files at server: ", data)
        return data

    def close(self):
        self.socket.send((3).to_bytes(2, 'big'))
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.active = False


def client(tcp_ip, tcp_port, mode: str, file_name: str):
    print("hi")
    cli = Client(tcp_ip, tcp_port)
    if mode == "load":
        cli.load(file_name)
    elif mode == "download":
        cli.save(file_name)
    cli.close()

# def client(TCP_IP, TCP_PORT, mode: str, file_name: str):
#     BUFFER_SIZE = 1024
#     DIR_FILES = 'client/'
#
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect((TCP_IP, TCP_PORT))
#
#     if mode == 'load':
#         f = open(file_name, 'r')
#         s.send((0).to_bytes(1, 'big'))
#         s.send(f.read().encode('utf-8'))
#     elif mode == 'save':
#         s.send((1).to_bytes(1, 'big'))
#         s.send(file_name.encode('utf-8'))
#         data = s.recv(BUFFER_SIZE)
#         load_file(DIR_FILES + "me", data.decode('utf-8'))
#
#     s.close()
