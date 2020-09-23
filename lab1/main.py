import asyncio
import threading


def _asyncio_thread(async_loop, fun, args):
    async_loop.run_until_complete(fun(args))


def do_tasks(async_loop, fun, args):
    """ Button-Event-Handler starting the asyncio part. """
    threading.Thread(target=_asyncio_thread, args=(async_loop, fun, args)).start()


if __name__ == "__main__":
    async_loop = asyncio.get_event_loop()

    from frames.TCPApp import TCPApp
    app = TCPApp(async_loop)
    app.mainloop()

    # print(TCP_IP, TCP_PORT)
    # tcp_ip: str = '127.0.0.1'
    # tcp_port: int = 5060
    # # thread1 = Thread(target=server, args=(TCP_IP, TCP_PORT))
    # # thread2 = Thread(target=client, args=(tcp_ip, tcp_port, 'load', 'b.txt'))
    # # thread1 = Thread(target=client, args=(tcp_ip, tcp_port, 'load', 'a.txt'))
    # cli = Client(tcp_ip, tcp_port)
    #
    # # cli.load('a.txt')
    # # cli.get_name_files()\
    # cli.save('b.txt')
    # cli.close()

    # thread2 = Thread(target=client, args=(TCP_IP, TCP_PORT, 'download', '1'))
    #
    # thread1.start()
    # thread2.start()
    # thread1.join()
    # thread2.join()
