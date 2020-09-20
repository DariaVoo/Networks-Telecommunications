from server import server
from client import client
from threading import Thread

# print('Введите IP сервера')
# TCP_IP = str(input())
# print('Введите PORT сервера')
# TCP_PORT = int(input())

if __name__ == "__main__":
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5053
    print(TCP_IP, TCP_PORT)
    thread1 = Thread(target=server, args=(TCP_IP, TCP_PORT))
    # thread2 = Thread(target=client, args=(TCP_IP, TCP_PORT, 'load', 'a.txt'))
    thread2 = Thread(target=client, args=(TCP_IP, TCP_PORT, 'save', '1'))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    # server(TCP_IP, TCP_PORT)
    # client(TCP_IP, TCP_PORT)

