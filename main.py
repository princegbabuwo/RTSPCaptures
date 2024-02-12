import os, sys, time, traceback
from turtle import width
from scripts import RTSP, FTP
from interface import GUI
from tkinter import *
from tkinter import ttk

class Main:
    def __init__(self) -> None:
        root = self.__root()
        rootFrame = self.__rootFrame(root)
        settings = self.__settings(rootFrame) 
        urlFrame, urlLabel, urlText = self.__RSTPURLFrame(rootFrame)
        imgBoxFrame, imgBox = self.__imageBox(rootFrame)
        captureButton = self.__captureButton(rootFrame)
        root.mainloop()

    def __root(self):
        root = Tk()
        root.title("RTSP Stream Capture")
        #root.columnconfigure(0, weight=1)
        #root.rowconfigure(0, weight=1)
        return root

    def __rootFrame(self, parent):
        frame = ttk.Frame(parent, height=500)
        frame.grid(column=0, row=0, sticky=(N, W, E, S))

    def __settings(self, parent):
        button = ttk.Button(parent, text="{-}", command=self.Events.OpenDialogForSettings)
        button.grid(column=2, row=0, sticky=(N, E))
    

    def __RSTPURLFrame(self, parent):
        frame = ttk.Frame(parent, borderwidth=1, relief='solid')
        frame.grid(column=1, row=0, sticky=(N, W, E))

        label = ttk.Label(frame, text="Enter RTSP URL:")
        label.grid(column=0, row=0, sticky=(N, W))

        text = ttk.Entry(frame)
        text.grid(column=0, row=1, sticky=(N, W))

        return frame, label, text
    
    def __imageBox(self, parent):
        style = ttk.Style()
        style.configure('Box.TFrame', background='red', padding=5, borderwidth=5, relief='raised')
        style.configure('Box.TLabel', background='grey', borderwith=2, relief='raised')

        frame = ttk.Frame(parent, width=100, height=100, style="Box.TFrame")
        frame.grid(column=1, row=1, sticky=(N, W, E, S))

        box = ttk.Label(frame, width=100, style='Box.TLabel')
        box.grid(column=0, row=0, sticky=(N, S))

        return frame, box
    
    def __captureButton(self, parent):
        button = ttk.Button(parent, text="START CAPTURING", command=self.Events.StartCapture)
        button.grid(column=1, row=2, sticky=(N, W, E))

        return button
    
    class Events:
        def OpenDialogForSettings(self):
            pass

        def StartCapture(self):
            pass

def main():
    Main()

def script():
    #return print ("script")
    #define apps inputs/vatiables
    rtsp_url = 'http://camera.buffalotrace.com/mjpg/video.mjpg'
    ftp_server = "ftp.dlptest.com"
    #ftp_port = 21
    ftp_user = "dlpuser"
    ftp_password = "rNrKYTX9g7z3RgJRmxWuGHbeu"
    ftp_dir = ""
    interval = 10

    try:
        stream = RTSP.OpenStream(rtsp_url=rtsp_url) #Open Stream
        print(stream)

        #initialize ftp server here
        ftp = FTP.Connect(ftp_server=ftp_server, ftp_user=ftp_user, ftp_password=ftp_password, ftp_dir=ftp_dir)

        #Capture Frame every 5 secs
        while True:
            ExecuteScript(ftp, stream)
            time.sleep(interval)
    except Exception as e: #Here we want to capture the errors as much as possible
        ExceptionHandler(sys, e, 1)

def ExecuteScript(ftp, stream):
    filename, image = stream.CaptureFrame() #Capture Image
    print(f"image: {image}" )
    if WriteImageLocally(filename, image):#Write image Locally
        print("Image Written to Machine")
    if ftp.UploadImageData(filename): #Upload File to FTP server
        print("Image Successfully uploaded")
    if DeleteLocalImage(filename): #Delete Image After upload
        print("Local Image Deleted")

def WriteImageLocally(filename, data):
    with open(filename, "wb") as f:
        f.write(data.tobytes())
    f.close()

def DeleteLocalImage(filename):
    os.remove(filename)
    return True
    

def ExceptionHandler(sys, e, exit_code):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    traceback.print_tb(exc_tb)
    print(f"\nError: {str(e)}")
    sys.exit(exit_code)

main()