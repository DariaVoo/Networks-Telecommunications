# import necessary packages

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from SMTP.utils.ft_done import ft_done
from not_send import PAAAS


def send_msg(to, subject, message):
    # create message object instance
    msg = MIMEMultipart()

    # message = "Thank you"

    # setup the parameters of the message
    password = PAAAS
    msg['From'] = "dariavvoroncova@gmail.com"
    msg['To'] = to
    msg['Subject'] = subject

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print(f"successfully sent email to {msg['To']}")
    ft_done(f"successfully sent email to {msg['To']}")
