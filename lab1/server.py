import socket
from file_op import load_file


class Server:
    def __init__(self, ip: int, port: int):
        self.port = port
        self.ip = ip
        self.DIR_FILES = 'server_files/'
        self.files = ["aaa"]
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

    def listen(self):
        while True:
            mode = self.conn.recv(2)
            mode = int.from_bytes(mode, 'big')
            if mode == 0:  # load
                self.load()
            elif mode == 1:  # download
                self.download()
            elif mode == 2:  # get_files
                self.get_all_files()

    def get_data(self):
        data = self.conn.recv(self.BUFFER_SIZE)
        tmp = 0
        while tmp:  # Могут быть большие файлы
            data += tmp
            tmp = self.conn.recv(self.BUFFER_SIZE)
        return data

    def load(self):  # Загрузить файл на сервак
        data = self.get_data()
        newfile = self.DIR_FILES + "1"
        self.files.append(newfile)
        load_file(newfile, data.decode('utf-8'))
        print("File was load to server")

    def download(self):  # Скачать файл с сервака
        data = self.get_data()
        f = open(self.DIR_FILES + data.decode('utf-8'), 'rb')
        self.conn.send(f.read())

    def get_all_files(self):
        f: str = ' '.join(self.files)
        print(type(f), f)
        fb: bytes = f.encode('utf-8')
        print(type(fb), f)
        # print(type(f.encode('utf-8')))
        self.conn.send(fb)

    def close(self):
        self.conn.close()


# def server(tcp_ip, tcp_port):
if __name__ == "__main__":
    try:
        tcp_ip: str = '127.0.0.1'
        tcp_port: int = 5064
        serv = Server(tcp_ip, tcp_port)
        serv.run()

        while True:
            serv.listen()
    finally:
        print("NOOOOOoo")
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
