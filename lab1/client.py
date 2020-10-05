import socket

from server import load_file
from utils.send_data import send_data


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
        send_data(self.socket, file_name.encode('utf-8'))

        f = open(file_name, 'rb')
        data = f.read()
        send_data(self.socket, data)

    def save(self, file_name: str, path: str):  # скачать с сервака
        """ Скачивание данных с сервера """
        self.socket.send((1).to_bytes(2, 'big'))
        send_data(self.socket, file_name.encode('utf-8'))

        data = self.get_data()
        load_file(path + '/' + file_name, data)
        print("File was downloaded to ", path)

    def get_len(self):
        data: str = ''
        tmp: str = ''
        while True:
            tmp = self.socket.recv(1).decode('utf-8')
            if tmp == '\0':
                return int(data)
            data += tmp
        return int(data)

    def get_data(self):
        len_data: int = self.get_len()
        data = self.socket.recv(len_data)
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
