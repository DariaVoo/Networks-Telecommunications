import base64
import imaplib
import poplib
import pprint
import quopri
import string
from email.header import decode_header
from email.parser import Parser

from pip._vendor.pyparsing import unicode

from not_send import PAAAS


class Client:
    def __init__(self, email: str):
        self.BUFFER_SIZE = 1024
        self.email = email
        self.server = poplib.POP3_SSL('pop.gmail.com')
        pop3_server_welcome_msg = self.server.getwelcome().decode('utf-8')
        print(pop3_server_welcome_msg)
        self.active = False

    def connect(self):
        self.server.user(self.email)
        self.server.pass_(PAAAS)
        self.active = True

    def get_msgs(self, rfc822=None):
        # parse the email content to a message object.
        # msg = Parser().parsestr(msg_content)

        # stat() function return email count and occupied disk size
        print('Messages: %s. Size: %s' % self.server.stat())
        # list() function return all email list
        resp, mails, octets = self.server.list()
        print(mails)

        # retrieve the newest email index number
        index = len(mails)
        index = len(mails) - 6
        # server.retr function can get the contents of the email with index variable value index number.
        resp, lines, octets = self.server.retr(index)

        # lines stores each line of the original text of the message
        # so that you can get the original text of the entire message use the join function and lines variable.
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        # now parse out the email object.
        msg = Parser().parsestr(msg_content)

        # get email from, to, subject attribute value.
        email_from = msg.get('From')
        email_to = msg.get('To')
        email_subject = msg.get('Subject')
        email_content = msg.get_payload()
        print('From ' + email_from)
        print('To ' + email_to)

        # parse subj
        bytes_subj, encoding = decode_header(email_subject)[0]
        if encoding is not None:
            email_subject = bytes_subj.decode(encoding)
        print('Subject ', email_subject)

        print('Content: ', end='')
        if msg.is_multipart():
            for part in email_content:
                # print('Content', m.get_papayload())
                charset = part.get_content_charset()

                if part.get_content_type() == 'text/plain':
                    text = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
                    print(text.strip())

                if part.get_content_type() == 'text/html':
                    html = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
                    print(html.strip())

        else:
            text = unicode(msg.get_payload(decode=True), msg.get_content_charset(), "ignore").encode('utf8', 'replace')
            print(text)

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
    cli.get_msgs()
    cli.close()

