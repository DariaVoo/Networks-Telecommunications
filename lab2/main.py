import asyncio

from do_ip_package import do_ip_package

if __name__ == "__main__":
    async_loop = asyncio.get_event_loop()

    from frames.GeneratorApp import GeneratorApp
    app = GeneratorApp(async_loop)
    app.mainloop()