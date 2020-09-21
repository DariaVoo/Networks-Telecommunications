import socket
from file_op import load_file


class Server:
    def __init__(self, ip: int, port: int):
        self.port = port
        self.ip = ip
        self.DIR_FILES = 'server_files/'
        self.files: list
        self.BUFFER_SIZE = 20  # Normally 1024, but we want fast response
        self.conn, self.addr_conn = 0, 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.socket.setblocking(1)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)
        print("Server listen port ", self.port)

        self.conn, self.addr_conn = self.socket.accept()
        print('Connection address:', self.addr_conn)

        mode = self.conn.recv(1)
        mode = int.from_bytes(mode, 'big')
        if mode == 0:  # load
            self.load()
        elif mode == 1:  # download
            self.download()

    def get_data(self):
        data = self.conn.recv(self.BUFFER_SIZE)
        tmp = 0
        while tmp:  # Могут быть большие файлы
            data += tmp
            tmp = self.conn.recv(self.BUFFER_SIZE)
        return data

    def load(self):  # Загрузить файл на сервак
        data = self.get_data()
        load_file(self.DIR_FILES + "1", data.decode('utf-8'))
        print("File was load to server")

    def download(self): # Скачать файл с сервака
        data = self.get_data()
        f = open(self.DIR_FILES + data.decode('utf-8'), 'rb')
        self.conn.send(f.read())

    def close(self):
        self.conn.close()


def server(tcp_ip, tcp_port):
    serv = Server(tcp_ip, tcp_port)
    serv.run()
    serv.close()


# def server(TCP_IP, TCP_PORT):
#     DIR_FILES = 'server_files/'
#     BUFFER_SIZE = 20  # Normally 1024, but we want fast response
#
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.setblocking(1)
#     s.bind((TCP_IP, TCP_PORT))
#     s.listen(1)
#     print("Server listen port ", TCP_PORT)
#
#     conn, addr = s.accept()
#     print('Connection address:', addr)
#     mode = conn.recv(1)
#     mode = int.from_bytes(mode, 'big')
#
#     data = conn.recv(BUFFER_SIZE)
#     tmp = 0
#     while tmp:  # Могут быть большие файлы
#         data += tmp
#         tmp = conn.recv(BUFFER_SIZE)
#
#     if mode == 0:  # load
#         load_file(DIR_FILES + "1", data.decode('utf-8'))
#     elif mode == 1:  # download
#         f = open(DIR_FILES + data.decode('utf-8'), 'r')
#         conn.send(f.read().encode('utf-8'))
#
#     conn.close()
