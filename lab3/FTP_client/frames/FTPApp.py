from tkinter import Tk

from FTP_client.frames.StartPage import StartPage


class FTPApp(Tk):
    def __init__(self, async_loop):
        Tk.__init__(self)
        self.async_loop = async_loop
        self._frame = None
        self.geometry("500x500")
        self.title("Lab6. FTP client")
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self, self.async_loop)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()
