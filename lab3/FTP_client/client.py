from ftplib import FTP

from FTP_client.utils.ft_done import ft_done


class Client:
    def __init__(self, mirror: str):
        self.BUFFER_SIZE = 1024
        self.ftp = FTP(mirror)
        self.active = False

    def connect(self):
        ft_done(self.ftp.login())
        self.active = True

    def load(self, file_name: str):  # загрузить на сервак
        """ Загрузка данных на сервер """
        with open(file_name, 'rb') as fobj:
            self.ftp.storbinary('STOR ' + file_name, fobj, 1024)

    def save(self, file_name: str, path: str):  # скачать с сервака
        """ Скачивание данных с сервера """

        with open(path + '/' + file_name, 'wb') as f:
            self.ftp.retrbinary('RETR ' + file_name, f.write)
        print("File was downloaded to ", path)

    def get_name_files(self):
        data = self.ftp.nlst()
        print("Files at server: ", data)
        return data

    def get_name_dirs(self, dir_name=''):
        if dir_name != '':
            self.ftp.cwd(dir_name)

        data_all = []
        self.ftp.dir("", data_all.append)
        # data = self.ftp.retrlines('LIST', data.append)
        data = [x.split()[-1] for x in data_all if x.startswith("d")]
        data += [x.split('/')[-1] for x in data_all if x.startswith("l")]
        print("Files at server: ", data)
        return data

    def close(self):
        self.ftp.quit()
        self.active = False


if __name__ == "__main__":
    cli = Client('ftp.cse.buffalo.edu')
    cli.connect()
    # cli.get_name_files(dir_name='users/bina')
    file = 'pub/Gnome'
    dirs = cli.get_name_dirs(dir_name='pub')
    # cli.save('bina_classschedule.csv', 'DOW')
    print(dirs[0].split('/')[-1])
