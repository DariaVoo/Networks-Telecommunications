from tkinter import Tk

from frames.StartPage import StartPage


class TCPApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.geometry("500x500")
        self.title("Lab1. TCP client-server.")
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()