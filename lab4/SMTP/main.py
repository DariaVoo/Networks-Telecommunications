import asyncio
from SMTP.frames.SMTPApp import SMTPApp

if __name__ == "__main__":
    async_loop = asyncio.get_event_loop()

    app = SMTPApp(async_loop)
    app.mainloop()
