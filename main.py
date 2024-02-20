from email import message
from logging import PlaceHolder
import os, sys, time, traceback
import threading
from turtle import rt
from scripts import RTSP, FTP
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import yaml
from threading import Thread

class Script:
    thread = None
    thread_flag = True
    rtsp_url = None
    ftp_server = None
    ftp_user = None
    ftp_password = None
    ftp_dir = None
    interval = None

    def getFTPServerConfiguration(self):
        config = None
        try: 
            with open('config.yaml', 'r') as f:
                config = yaml.safe_load(f)
            f.close()
        except FileNotFoundError: 
            return self.defineYamlFile('', '', '', '', '')
        else: return config

    def checkFTPServerConfiguration(self):
        try: 
            with open('config.yaml', 'r') as f:
                config = yaml.safe_load(f)
            f.close()
        except FileNotFoundError: return False
        except Exception as e:
            self.ExceptionHandler(sys, e, 1)
            return False
        else: return True

    def updateConfigurationFile(self):
        #if not script.checkFTPServerConfiguration(): pass
            #create yaml file
        data = self.defineYamlFile(gui.SettingsWindows.serverEntry.get(), 
                    gui.SettingsWindows.userEntry.get(),
                    gui.SettingsWindows.passwordEntry.get(),
                    gui.SettingsWindows.dirEntry.get(),
                    gui.SettingsWindows.intervalEntry.get())
        #return print(data)

        with open('config.yaml', 'w') as f:
            yaml.dump(data, f, allow_unicode=True)
        f.close()
        
        return True

    def defineYamlFile(self, server, user, password, dir, interval):
        return {
            'server': server,
            'user': user,
            'password': password,
            'dir': dir,
            'interval': interval,
        }
    
    def updateRTSPUrlOnFile(self, url):
        config = self.getFTPServerConfiguration()
        config['url'] = url

        with open('config.yaml', 'w') as f:
            yaml.dump(config, f, allow_unicode=True)
        f.close()
        return config
    
    #CODE startCaptureProcess
    def startCaptureProcess(self, rtsp_url = rtsp_url, ftp_server=ftp_server, ftp_user=ftp_user, ftp_password=ftp_password, ftp_dir=ftp_dir, interval=interval):
        """
        self.rtsp_url = rtsp_url
        self.ftp_server = ftp_Server
        self.ftp_user = ftp_user
        self.ftp_password = ftp_password
        self.ftp_dir = ftp_dir
        self.interval = interval
        """

        def callBack(rtsp_url, ftp_server, ftp_user, ftp_password, ftp_dir, interval):
            print(rtsp_url)
            print(ftp_server)
            print(ftp_user)
            print(ftp_password)
            print(interval)
            interval = int(interval)
            try:
                stream = RTSP.OpenStream(rtsp_url=rtsp_url) #Open Stream
                print(stream)

                #initialize ftp server here
                ftp = FTP.Connect(ftp_server=ftp_server, ftp_user=ftp_user, ftp_password=ftp_password, ftp_dir=ftp_dir)

                #Capture Frame every 5 secs
                while script.thread_flag:
                    self.captureAndUpload(ftp, stream, interval)
                    time.sleep(1)
                else:
                    ftp.close()
                    stream.release()
            except Exception as e: #Here we want to capture the errors as much as possible
                messagebox.showinfo(message=e)
                self.ExceptionHandler(sys, e, 1)

        self.thread = threading.Thread(target=callBack, args=(rtsp_url, ftp_server, ftp_user, ftp_password, ftp_dir, interval), daemon=True)
        self.thread.start()

    def captureAndUpload(self, ftp, stream, interval):
        filename, frame, image = stream.CaptureFrame() #Capture Image
        print(f'frame: {frame}')
        print(f"image: {image}" )

        if self.WriteImageLocally(filename, image.tobytes()):#Write image Locally
            print("Image Written to Machine")

        #show image on canvas
        picture = ImageTk.PhotoImage(Image.fromarray(frame))
        #print(picture) 
        gui.HomeWindows.mediaImage.config(image=picture)
        
        if ftp.UploadImageData(filename): #Upload File to FTP server
            print("Image Successfully uploaded")

        time.sleep(interval-1) #put system to rest
        gui.HomeWindows.mediaImage.config(image=None)
        if self.DeleteLocalImage(filename): #Delete Image After upload
            print("Local Image Deleted")
        

    def WriteImageLocally(self, filename, data):
        with open(filename, "wb") as f:
            f.write(data)
        f.close()
        return 

    def DeleteLocalImage(self, filename):
        os.remove(filename)
        return True

    #CODE Exception Handler
    def ExceptionHandler(self, sys, e, exit_code):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        traceback.print_tb(exc_tb)
        print(f"\nError: {str(e)}")
        sys.exit(exit_code)

class GUI:
    def __init__(self) -> None:
        self.HomeWindows = self.HomeWindows()
        self.SettingsWindows = self.SettingsWindows()
        self.Events = self.Events()

    #CODE HomeWindows
    class HomeWindows:
        def draw(self) -> None:
            self.window = Tk()
            self.window.title("RTSP Stream Capture")
            self.window.resizable(False, False)
            #config = 
            self.window.after(1, lambda: gui.Events.onWindowsOpen())

            style = ttk.Style()
            style.configure('url.TEntry', padding=(10, 5))
            style.configure('capture.TButton', font=("Arial", 12, "bold"), padding=(0, 12))
            style.configure('icon.TButton', padding=5)

            windowFrame = ttk.Frame(self.window, padding=20)

            #url Box Frame
            urlFrame = ttk.Frame(windowFrame, borderwidth=1, relief='solid', padding=10)
            urlLabel = ttk.Label(urlFrame, text="Enter RTSP URL:", font=("Arial", 12, "bold"))
            self.urlText = ttk.Entry(urlFrame, width=80, style='url.TEntry')

            #mediaCanvas
            mediaFrame = ttk.Frame(windowFrame, padding=20)
            self.mediaCanvas = Canvas(mediaFrame, width=480, height=270, background='gray75')
            self.mediaImage = ttk.Label(mediaFrame, background='red')

            #ButtonsFrame
            buttonFrame = ttk.Frame(windowFrame)
            self.captureButton = ttk.Button(buttonFrame, text="START CAPTURE", width=52, style='capture.TButton', command=lambda: (gui.Events.StartCapture(self.urlText)))
            settingsIcon = PhotoImage(file=os.path.abspath('assets/settings.png'))
            settingsButton = ttk.Button(buttonFrame, image=settingsIcon, width=5, style='icon.TButton', command=gui.Events.OpenDialogForSettings)

            windowFrame.grid(column=0, row=0)

            urlFrame.grid(column=0, row=0, sticky=EW) #parent=>rootFrame
            urlLabel.grid(column=0, row=0, sticky=W)
            self.urlText.grid(column=0, row=1, columnspan=2, sticky=EW)

            mediaFrame.grid(column=0, row=1) #parent=>rootFrame
            self.mediaCanvas.grid(column=0, row=0, sticky=NSEW) #parent=>mediaFrame
            self.mediaImage.grid(column=0, row=0, sticky=NSEW)

            buttonFrame.grid(column=0, row=2, sticky=EW) #parent=>rootFrame
            self.captureButton.grid(column=0, row=0)
            settingsButton.grid(column=1, row=0)
    
            #Here check if server have been configured
            if not script.checkFTPServerConfiguration():
                pass#settingsWindows = GUI().SettingsWindows().__draw()
            self.window.mainloop()

        def call(self):
            #return 0
            gui.Events.BeforeWindowsOpen()
            self.draw()
            #self.window.mainloop()

        def updateCaptureButton(self, state):
            print('am in update capture')
            match state:
                case 'start':
                    self.captureButton.configure(text='START CAPTURE', command=lambda: gui.Events.StartCapture(self.urlText))
                case 'stop':
                    def __command():
                        #rstp
                        script.thread_flag = False
                        script.thread.join()
                        self.updateCaptureButton('start')
                    self.captureButton.configure(text='STOP CAPTURE', command=__command)


    class SettingsWindows:
        def __draw(self, config) -> None:
            self.window = Toplevel(gui.HomeWindows.window)
            self.window.title("RTSP Stream Capture: Settings")
            self.window.resizable(False, False)
            self.window.wm_attributes("-topmost", True)
            self.window.protocol("WM_DELETE_WINDOW", gui.SettingsWindows.dismiss)

            style = ttk.Style()
            style.configure("number_entry.TEntry", validchars="0123456789")

            self.windowFrame = ttk.Frame(self.window, padding=20)
            self.windowFrame.grid(column=0, row=0, sticky=NSEW)

            self.title = ttk.Label(self.windowFrame, text='Configure FTP Server', font=("Arial", 12, "bold"))
            self.title.grid(column=0, row=0, sticky=W)

            self.serverFrame = ttk.Frame(self.windowFrame, padding=(0, 10))
            self.serverFrame.grid(column=0, row=1, sticky=W)
            self.serverLabel = ttk.Label(self.serverFrame, text="FTP Server:")
            self.serverEntry = ttk.Entry(self.serverFrame, width=40)
            self.serverEntry.insert(0, config['server'])
            self.serverLabel.grid(column=0, row=0, sticky=W)
            self.serverEntry.grid(column=0, row=1, sticky=W)
            #Add LineThrough

            self.userFrame = ttk.Frame(self.windowFrame, padding=(0, 0, 0, 10))
            self.userFrame.grid(column=0, row=2, sticky=W)
            self.userLabel = ttk.Label(self.userFrame, text="Username:")
            self.userEntry = ttk.Entry(self.userFrame, width=40)
            self.userEntry.insert(0, config['user'])
            self.userLabel.grid(column=0, row=0, sticky=W)
            self.userEntry.grid(column=0, row=1, sticky=W)

            self.passwordFrame = ttk.Frame(self.windowFrame, padding=(0, 0, 0, 10))
            self.passwordFrame.grid(column=0, row=3, sticky=W)
            self.passwordLabel = ttk.Label(self.passwordFrame, text="Password:")
            self.passwordEntry = ttk.Entry(self.passwordFrame, width=40, show="*")
            self.passwordEntry.insert(0, config['password'])
            self.passwordLabel.grid(column=0, row=0, sticky=W)
            self.passwordEntry.grid(column=0, row=1, sticky=W)

            self.dirFrame = ttk.Frame(self.windowFrame, padding=(0, 0, 0, 10))
            self.dirFrame.grid(column=0, row=4, sticky=W)
            self.dirLabel = ttk.Label(self.dirFrame, text="Directory Path")
            self.dirEntry = ttk.Entry(self.dirFrame, width=40)
            self.dirEntry.insert(0, config['dir'])
            self.dirLabel.grid(column=0, row=0, sticky=W)
            self.dirEntry.grid(column=0, row=1, sticky=W)

            self.intervalFrame = ttk.Frame(self.windowFrame, padding=(0, 0, 0, 10))
            self.intervalFrame.grid(column=0, row=5, sticky=W)
            self.intervalLabel = ttk.Label(self.intervalFrame, text="Set Capture Intervals(sec):")
            self.intervalEntry = ttk.Entry(self.intervalFrame, width=22, validate="key")
            self.intervalEntry.insert(0, config['interval'])
            self.intervalLabel.grid(column=0, row=0, sticky=W)
            self.intervalEntry.grid(column=0, row=1, sticky=W)
            #Add LineThrough

            self.saveButton = ttk.Button(self.windowFrame, text='save', command=gui.Events.saveServerInformation)
            self.saveButton.grid(column=0, row=6, sticky=W)

        """
        def __numberChar(self, new_text):
            if not new_text.isdigit():
                return False
            return True
        """

        def show(self, config):
            gui.SettingsWindows.__draw(config)
            gui.SettingsWindows.window.grab_set()
            gui.SettingsWindows.window.wait_window()
        
        def dismiss(self):
            #print('Im in dismiss')
            if not script.checkFTPServerConfiguration():
                messagebox.showinfo(message='Configure FTP Server Information!')
                return False
            gui.SettingsWindows.window.grab_release()
            gui.SettingsWindows.window.destroy()

        def validateForm(self):
            if gui.SettingsWindows.serverEntry.get() == '':
                messagebox.showinfo(message='Enter FTP server address')
                return False
            if gui.SettingsWindows.userEntry.get() == '':
                messagebox.showinfo(message='Enter FTP server username')
                return False
            if gui.SettingsWindows.passwordEntry.get() == '':
                messagebox.showinfo(message='Enter FTP server password')
                return False
            if int(gui.SettingsWindows.validateIntergerEntry()) < 1:
                messagebox.showinfo(message='Intervals should be a positive number')
                return False
            return True
        
        def validateIntergerEntry(self):
            try: interval = int(gui.SettingsWindows.intervalEntry.get().strip())
            except ValueError: return 0
            else: return interval

    class Events:
        GUI = None
        HomeWindows = None
        SettingsWindow  = None
        def __init__(self, GUI=GUI, HomeWindows=HomeWindows, SettingsWindow=SettingsWindow) -> None:
            self.GUI = self.GUI
            self.HomeWindows = HomeWindows
            self.SettingsWindow = SettingsWindow
            print(f'Settings Windows @-Event: {self.SettingsWindow}')

        def onWindowsOpen(self):
            if not script.checkFTPServerConfiguration():
                gui.Events.OpenDialogForSettings()

        def OpenDialogForSettings(self):
            config = script.getFTPServerConfiguration()
            #print (f'Config: {config}')
            gui.SettingsWindows.show(config)

        def saveServerInformation(self):
            if gui.SettingsWindows.validateForm():
                script.updateConfigurationFile()
                messagebox.showinfo(message='Server Information updated!')
                gui.SettingsWindows.dismiss()

        def StartCapture(self, entry):
            url = entry.get()
            if url == "":
                return messagebox.showinfo(message='Enter RTSP URL')

            script.updateRTSPUrlOnFile(url)
            config = script.getFTPServerConfiguration()
            gui.HomeWindows.updateCaptureButton('stop')
            script.thread_flag = True
            script.startCaptureProcess(rtsp_url=config['url'], ftp_server=config['server'], 
                    ftp_user=config['user'], ftp_password=config['password'], 
                    ftp_dir=config['dir'], interval=config['interval'])

script = Script()
gui = GUI()

def main():
    gui.HomeWindows.draw()
    pass

def _script():
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
    
"""
def ExceptionHandler(sys, e, exit_code):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    traceback.print_tb(exc_tb)
    print(f"\nError: {str(e)}")
    sys.exit(exit_code)
"""

main()