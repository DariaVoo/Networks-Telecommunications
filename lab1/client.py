import socket
from server import load_file


def client(TCP_IP, TCP_PORT, mode:str, file_name:str):
  BUFFER_SIZE = 1024
  DIR_FILES = 'client/'
  MESSAGE = "Hello, World!"

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
