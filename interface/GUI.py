from tkinter import *
from tkinter import ttk

#tkinter._test()
class Homepage:
    def __init__(self) -> None:
        root = self.__root()
        rootFrame = self.__rootFrame(root)
        
        urlFrame = self.__RSTPURLFrame(rootFrame)

        root.mainloop()

    def __root(self):
        root = Tk()
        root.title("RTSP Stream Capture")
        #root.columnconfigure(0, weight=1)
        #root.rowconfigure(0, weight=1)
        return root

    def __rootFrame(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(column=0, row=0, sticky=(N, W, E, S))
    

    def __RSTPURLFrame(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(column=1, row=0, sticky=(N, W, E))

        label = ttk.Label(frame, text="Enter RTSP URL")
        label.grid(column=0, row=0, sticky=(N, W))

        text = ttk.Entry

        return frame
