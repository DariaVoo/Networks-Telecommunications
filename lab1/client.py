import socket
from server import load_file


class Client:
    def __init__(self, ip: int, port: int):
        self.TCP_PORT = port
        self.TCP_IP = ip
        self.BUFFER_SIZE = 1024
        self.DIR_FILES = 'client/'

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.TCP_IP, self.TCP_PORT))

    def load(self, file_name: str):
        f = open(file_name, 'r')
        self.socket.send((0).to_bytes(1, 'big'))
        self.socket.send(f.read().encode('utf-8'))

    def save(self, file_name: str):
        self.socket.send((1).to_bytes(1, 'big'))
        self.socket.send(file_name.encode('utf-8'))
        data = self.socket.recv(self.BUFFER_SIZE)
        load_file(self.DIR_FILES + "me", data.decode('utf-8'))

    def close(self):
        self.socket.close()


def client(TCP_IP, TCP_PORT, mode: str, file_name: str):
    BUFFER_SIZE = 1024
    DIR_FILES = 'client/'
    MESSAGE = "Hello, World!"

    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    if mode == 'load':
        f = open(file_name, 'r')
        s.send((0).to_bytes(1, 'big'))
        s.send(f.read().encode('utf-8'))
    elif mode == 'save':
        s.send((1).to_bytes(1, 'big'))
        s.send(file_name.encode('utf-8'))
        data = s.recv(BUFFER_SIZE)
        load_file(DIR_FILES + "me", data.decode('utf-8'))

    s.close()
