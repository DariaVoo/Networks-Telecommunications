import asyncio

from HTTP_client.frames.HTTPApp import HTTPApp

if __name__ == "__main__":
    async_loop = asyncio.get_event_loop()

    app = HTTPApp(async_loop)
    app.mainloop()
