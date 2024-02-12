from tkinter import *
from tkinter import ttk

class Homepage:
    def __init__(self) -> None:
        root = self.__root()
        rootFrame = self.__rootFrame(root)
        settings = self.__settings(rootFrame) 
        urlFrame, urlLabel, urlText = self.__RSTPURLFrame(rootFrame)
        captureButton = self.__captureButton(rootFrame)

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

    def __settings(self, parent):
        button = ttk.Button(parent, text="{-}", command=self.__settingsDialog)
        button.grid(column=2, row=0, sticky=(N, E))
    

    def __RSTPURLFrame(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(column=1, row=0, sticky=(N, W, E))

        label = ttk.Label(frame, text="Enter RTSP URL:")
        label.grid(column=0, row=0, sticky=(N, W))

        text = ttk.Entry(frame)
        text.grid(column=0, row=1, sticky=(N, W))

        return frame, label, text
    
    def __captureButton(self, parent):
        button = ttk.Button(parent, text="START CAPTURING", command=self.__startCapturing)
        button.grid(column=1, row=3, sticky=(N, W, E))

        return button
    
    def __settingsDialog(self):
        pass

    def __startCapturing(self):
        pass
