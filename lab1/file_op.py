def load_file(file_name, data: bytearray):
    """ Функция загрузки данных(файла) на сервер """
    try:
        f = open(file_name, 'wb')
        f.write(data)
        f.close()
    except Exception as e:
        print(e)
    return 1


def save_file(file_name):
    """ Функция чтения данных(файла) """
    try:
        f = open(file_name, 'rb')
        data = f.read()
        f.close()
    except Exception as e:
        print(e)
    return data
