import socket
import os
import os.path

class Server:
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setblocking(True)
        self.s.bind((host, port))
        self.s.listen(10)

        self.active_connection = None
        self.active_connection_address = None

    def accept(self):
        self.active_connection, self.active_connection_address = self.s.accept()
        print('Server: Connection established with address', self.active_connection_address)

    def send_file_names(self):
        file_names = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), f))]

        file_names.append('\0')

        print('Server: ', ' '.join(file_names).encode('utf-8'))

        byte_file_names = ' '.join(file_names).encode('utf-8')

        self.active_connection.send(byte_file_names)

    def get_file_name(self):
        # file_name = ''
        temp_byte_array = bytes()
        while True:
            # if file_name.endswith('\0'):
            if temp_byte_array.endswith(b'\0'):
                break
            data = self.active_connection.recv(1)
            temp_byte_array += data
            # file_name += data.decode('utf-8')
        print(temp_byte_array)
        file_name = temp_byte_array[:-1].decode('utf-8')
        print('Server: File name recieved', file_name)
        # cut the absolute path
        return file_name.split(sep='/')[-1]

    # save to the client
    def save_file(self):
        file_name = self.get_file_name()

        print('Server: file name', file_name)

        path_to_file = os.path.join(os.getcwd(), file_name)

        print('Server: path to file', path_to_file)

        load(self.active_connection, path_to_file)

    # load to the server
    def load_file(self):
        file_name = self.get_file_name()

        print('Server: file name', file_name)

        path_to_file = os.path.join(os.getcwd(), file_name)

        print('Server: path to file', path_to_file)

        save(self.active_connection, path_to_file)

    def get_code(self):
        temp = ''
        while True:
            if temp.endswith('end'):
                break
            data = self.active_connection.recv(1)
            temp += data.decode('utf-8')
        return int(temp[:-4]) 

    def process_connection(self):
        while True:
            # try:
            code = self.get_code()
            # except:
                # break
            print('Server: Code received ', code)

            if code == 0:
                self.send_file_names()
                print('Server: File names sent')
            if code == 1:
                self.save_file()
            if code == 2:
                self.load_file()
            if code == 3:
                print('Server: connection closed')
                self.active_connection.close()
                break

    def serve(self):
        while True:
            self.accept()
            self.process_connection()


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._active = False

    def connect(self, address, port):
        self.s.connect((address, port))
        self._active = True
        print('Client: connection established')

    def is_active(self):
        return self._active

    def get_file_names(self):
        # 0 - code for receiving file names
        self.s.send('0 end'.encode('utf-8'))

        temp = ''
        while True:
            if temp.endswith('\0'):
                break
            data = self.s.recv(1)
            temp += data.decode('utf-8')

        print('Client: file names received ', temp.split())

        return temp.split()[:-1]

    # save to the client
    def save_file(self, path_to_file):
        # 1 - code for saving to the client
        self.s.send('1 end'.encode('utf-8'))

        self.s.send((path_to_file + '\0').encode('utf-8'))

        save(self.s, path_to_file)

    # load to the server
    def load_file(self, path_to_file):
        # 2 - code for loading to the server
        self.s.send('2 end'.encode('utf-8'))

        self.s.send((path_to_file + '\0').encode('utf-8'))

        load(self.s, path_to_file)

    def close(self):
        # 3 - code for closing the connection
        self.s.send('3 end'.encode('utf-8'))

        # self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
        # create a new socket for the client as the old one is no more
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._active = False

def load(from_, path_to_file):
    with open(path_to_file, 'rb') as f:
        temp = f.read()
        print('Load: ', temp.decode('utf-8'))
        from_.send(temp)
    from_.send(b'\0')
        
def save(from_, path_to_file):
    temp = ' '
    debug_str = ''
    with open(path_to_file, 'wb') as f:
        while True: 
            if temp == b'\0':
                break
            temp = from_.recv(1)
            print(temp.decode('utf-8'), end='')
            debug_str += temp.decode('utf-8')
            if temp != b'\0':
                f.write(temp)
    print()    
    print('Save: saved file contents: ', debug_str)