import asyncio

from POP3.frames.POP3App import POP3App

if __name__ == "__main__":
    async_loop = asyncio.get_event_loop()

    app = POP3App(async_loop)
    app.mainloop()
