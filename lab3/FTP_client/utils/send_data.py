def send_data(_src, data):
    _src.send(str(len(data)).encode('utf-8'))
    _src.send('\0'.encode('utf-8'))
    _src.send(data)