import os
import socket

from file_op import load_file
from utils.send_data import send_data


class Server:
    def __init__(self, ip: int, port: int):
        self.port = port
        self.ip = ip
        self.DIR_FILES = 'server_files/'
        self.files = os.listdir(self.DIR_FILES)
        self.BUFFER_SIZE = 30  # Normally 1024, but we want fast response
        self.conn, self.addr_conn = 0, 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run()

    def run(self):
        self.socket.setblocking(1)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)
        print("Server listen port ", self.port)

    def accept(self):
        self.conn, self.addr_conn = self.socket.accept()
        print('Connection address:', self.addr_conn)

    def listen(self):
        try:
            while True:
                mode = self.conn.recv(2)
                mode = int.from_bytes(mode, 'big')
                if mode == 0:  # load
                    self.load()
                elif mode == 1:  # download
                    self.download()
                elif mode == 2:  # get_files
                    self.get_all_files()
                elif mode == 3:  # close
                    self.close()
        finally:
            return

    def get_len(self):
        data: str = ''
        tmp: str = ''
        while True:
            tmp = self.conn.recv(1).decode('utf-8')
            if tmp == '\0':
                return int(data)
            data += tmp
        return int(data)

    def get_data(self):
        len_data: int = self.get_len()
        data = self.conn.recv(len_data)
        return data

    def get_file_name(self):
        file_name = self.get_data().decode('utf-8')
        print('Server: File name recieved', file_name)
        return file_name.split(sep='/')[-1]

    def load(self):
        """ Загрузить файл на сервер """
        newfile = self.DIR_FILES + self.get_file_name()
        print("File will be load to", newfile)
        data = self.get_data()
        load_file(newfile, data)
        print("File was load to server")
        self.files.append(newfile)
        # нужно отобразить на экране

    def download(self):
        """ Скачать файл с сервера """
        data = self.get_data()
        filename = self.DIR_FILES + data.decode('utf-8')

        print("Want to Download", filename)
        f = open(filename, 'rb')
        data = f.read()
        send_data(self.conn, data)
        print("Download", filename, " done")

    def get_all_files(self):
        """ Получить список файлов на сервере"""
        f: str = ' '.join(self.files)
        fb: bytes = f.encode('utf-8')
        send_data(self.conn, fb)

    def serve(self):
        while True:
            self.accept()
            self.listen()

    def close(self):
        self.conn.close()
        print("Active connection closed")


if __name__ == "__main__":
    try:
        tcp_ip: str = '127.0.0.1'
        tcp_port: int = 5060
        serv = Server(tcp_ip, tcp_port)
        serv.serve()
    finally:
        print("NOOOOOoo")
        serv.close()
