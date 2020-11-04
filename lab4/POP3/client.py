import poplib
from email.header import decode_header
from email.parser import Parser
from email.message import Message

from pip._vendor.pyparsing import unicode

from not_send import PAAAS


def decode_field(field: str):
    """ Парсинг полей сообщения"""
    bytes_subj, encoding = decode_header(field)[0]
    if encoding is not None:
        field = bytes_subj.decode(encoding)
    return field


class Client:
    def __init__(self, email: str):
        self.BUFFER_SIZE = 1024
        self.email = email
        self.server = poplib.POP3_SSL('pop.gmail.com')
        pop3_server_welcome_msg = self.server.getwelcome().decode('utf-8')
        print(pop3_server_welcome_msg)
        self.active = False
        self.msgs = []

    def connect(self):
        self.server.user(self.email)
        self.server.pass_(PAAAS)
        self.active = True

    def get_msgs(self):
        # stat() function return email count and occupied disk size
        print('Messages: %s. Size: %s' % self.server.stat())
        # list() function return all email list
        resp, mails, octets = self.server.list()
        print(mails)

        # retrieve the newest email index number
        for index in range(1, len(mails) + 1):
            # server.retr function can get the contents of the email with index variable value index number.
            resp, lines, octets = self.server.retr(index)

            # lines stores each line of the original text of the message
            # so that you can get the original text of the entire message use the join function and lines variable.
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            # now parse out the email object.
            msg = Parser().parsestr(msg_content)

            # get email from, to, subject attribute value.
            email_from = decode_field(msg.get('From'))
            email_to = decode_field(msg.get('To'))
            email_subject = decode_field(msg.get('Subject'))
            email_content = self.get_msg_content(msg)

            print('From ' + email_from)
            print('To ' + email_to)
            print('Subject ', email_subject)
            print('Content: ', email_content)
            print()
            self.msgs.append((email_from, email_to, email_subject, email_content))

        return self.msgs

    def get_msg_content(self, msg: Message):
        """ Парсинг содержания сообщения"""
        email_content = msg.get_payload()
        if msg.is_multipart():
            for part in email_content:
                # print('Content', m.get_papayload())
                charset = part.get_content_charset()

                if part.get_content_type() == 'text/plain':
                    text = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
                    return text.strip()

                if part.get_content_type() == 'text/html':
                    html = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
                    return html.strip()

        else:
            text = unicode(msg.get_payload(decode=True), msg.get_content_charset(), "ignore").encode('utf8', 'replace')
            return text.strip()

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
        self.server.close()
        self.active = False


if __name__ == "__main__":
    cli = Client("dariavvoroncova@gmail.com")
    cli.connect()
    ms = cli.get_msgs()
    print(ms)
    cli.close()

