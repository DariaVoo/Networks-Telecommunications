import asyncio

from FTP_client.frames.FTPApp import FTPApp

if __name__ == "__main__":
    async_loop = asyncio.get_event_loop()

    app = FTPApp(async_loop)
    app.mainloop()
