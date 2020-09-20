import socket


def load_file(file_name, data):
  f = open(file_name, 'w')
  
  f.write(data)
  f.close
  return 1

def save_file(file_name):
  f = open(file_name, 'r')

  data = f.read()
  f.close()
  return data

def server(TCP_IP, TCP_PORT):
  DIR_FILES = 'server_files/'
  BUFFER_SIZE = 20  # Normally 1024, but we want fast response
 
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setblocking(1)
  s.bind((TCP_IP, TCP_PORT))
  s.listen(1)
  print("Server listen port ", TCP_PORT)

  conn, addr = s.accept()
  print('Connection address:', addr)
  mode = conn.recv(1)
  mode = int.from_bytes(mode, 'big')
  
  data = conn.recv(BUFFER_SIZE)
  tmp = 0 
  while tmp: # Могут быть большие файлы
        data += tmp
        tmp = conn.recv(BUFFER_SIZE)

  if mode == 0: # load
    load_file(DIR_FILES + "1", data.decode('utf-8'))
  elif mode == 1: # download
    f = open(DIR_FILES + data.decode('utf-8'), 'r')
    conn.send(f.read().encode('utf-8'))
        

  conn.close()