def load_file(file_name, data):
    """ Функция загрузки данных(файла) на сервер """
    try:
        f = open(file_name, 'wb')
        f.write(bytes(data, 'utf-8'))
        f.close()
    except FileNotFoundError:
        print('File Not found')
    except IOError:
        print('Something else')
    return 1


def save_file(file_name):
    """ Функция чтения данных(файла) """
    try:
        f = open(file_name, 'rb')
        data = f.read()
        f.close()
    except FileNotFoundError:
        print('Not found')
    except IOError:
        print('Something else')
    return data
