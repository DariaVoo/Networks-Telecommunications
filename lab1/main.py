import asyncio

if __name__ == "__main__":
    async_loop = asyncio.get_event_loop()

    from frames.TCPApp import TCPApp
    app = TCPApp(async_loop)
    app.mainloop()
