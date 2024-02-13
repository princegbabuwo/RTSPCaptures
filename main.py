import os, sys, time, traceback
from turtle import width
from scripts import RTSP, FTP
from interface import GUI
from tkinter import *
from tkinter import ttk

class GUI:
    def Homepage(self) -> None:
        root = Tk()
        root.title("RTSP Stream Capture")
        root.resizable(False, False)

        style = ttk.Style()
        style.configure('url.TEntry', padding=(10, 5))
        style.configure('capture.TButton', font=("Arial", 12, "bold"), padding=(0, 12))
        style.configure('icon.TButton', padding=5)

        rootFrame = ttk.Frame(root, padding=20)

        #url Box Frame
        urlFrame = ttk.Frame(rootFrame, borderwidth=1, relief='solid', padding=10)
        urlLabel = ttk.Label(urlFrame, text="Enter RTSP URL:", font=("Arial", 12, "bold"))
        #urlTextFrame = ttk.Frame(urlFrame, background='white')
        urlText = ttk.Entry(urlFrame, width=80, style='url.TEntry')

        #mediaCanvas
        mediaFrame = ttk.Frame(rootFrame, padding=20)
        mediaCanvas = Canvas(mediaFrame, width=480, height=270, background='gray75')

        #ButtonsFrame
        buttonFrame = ttk.Frame(rootFrame)
        capturButton = ttk.Button(buttonFrame, text="START CAPTURE", width=52, style='capture.TButton' ,command=self.Events.StartCapture)
        settingsIcon = PhotoImage(file='assets/settings.png')
        settingsButton = ttk.Button(buttonFrame, image=settingsIcon, text="settings", width=5, style='icon.TButton', command=self.Events.OpenDialogForSettings)

        rootFrame.grid(column=0, row=0)

        urlFrame.grid(column=0, row=0, sticky=EW) #parent=>rootFrame
        urlLabel.grid(column=0, row=0, sticky=W)
        urlText.grid(column=0, row=1, columnspan=2, sticky=EW)

        mediaFrame.grid(column=0, row=1) #parent=>rootFrame
        mediaCanvas.grid(column=0, row=0, sticky=NSEW) #parent=>mediaFrame

        buttonFrame.grid(column=0, row=2, sticky=EW) #parent=>rootFrame
        capturButton.grid(column=0, row=0)
        settingsButton.grid(column=1, row=0)


        root.mainloop()

    def __root(self):
        root = Tk()
        root.title("RTSP Stream Capture")
        #root.columnconfigure(0, weight=1)
        #root.rowconfigure(0, weight=1)
        return root

    def __rootFrame(self, parent):
        frame = ttk.Frame(parent, padding=(20, 20, 20, 20))
        frame.grid(column=0, row=0)
    

    def __RSTPURLFrame(self, parent):
        frame = ttk.Frame(parent, borderwidth=1, relief='solid', width=200, height=100)
        frame.grid(column=0, row=0, sticky=EW)

        label = ttk.Label(frame, text="Enter RTSP URL:")
        label.grid(column=0, row=0, sticky=W)

        text = ttk.Entry(frame, width=50)
        text.grid(column=0, row=1, sticky=W)

        return frame, label, text
    
    def __settings(self, parent):
        button = ttk.Button(parent, text="{-}", command=self.Events.OpenDialogForSettings)
        button.grid(column=2, row=1)
    
    def __imageBox(self, parent):
        style = ttk.Style()
        style.configure('Box.TFrame', background='red', padding=5, borderwidth=5, relief='raised')
        style.configure('Box.TLabel', background='grey', borderwith=2, relief='raised')

        frame = ttk.Frame(parent, style="")
        frame.grid(column=2, row=2)

        box = ttk.Label(frame, style='')
        box.grid(column=1, row=1,)

        return frame, box
    
    def __captureButton(self, parent):
        button = ttk.Button(parent, text="START CAPTURING", command=self.Events.StartCapture)
        button.grid(column=2, row=3)

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