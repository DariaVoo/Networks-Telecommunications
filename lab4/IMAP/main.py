import asyncio

from IMAP.frames.IMAPApp import IMAPApp

if __name__ == "__main__":
    async_loop = asyncio.get_event_loop()

    app = IMAPApp(async_loop)
    app.mainloop()
