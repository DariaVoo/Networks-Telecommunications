def load_file(file_name, data):
    """ Функция загрузки данных(файла) на сервер """
    f = open(file_name, 'wb')
    f.write(bytes(data, 'utf-8'))
    f.close()
    return 1


def save_file(file_name):
    """ Функция чтения данных(файла) """
    f = open(file_name, 'rb')
    data = f.read()
    f.close()
    return data
