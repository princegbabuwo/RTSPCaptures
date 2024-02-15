from logging import PlaceHolder
import os, sys, time, traceback
#from turtle import width
from scripts import RTSP, FTP
#from interface import GUI
from tkinter import *
from tkinter import ttk, messagebox
import yaml

class Script:
    def getFTPServerConfiguration(self):
        pass

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
        data = script.defineYamlFile(gui.SettingsWindows.serverEntry.get(), 
                    gui.SettingsWindows.userEntry.get(),
                    gui.SettingsWindows.passwordEntry.get(),
                    gui.SettingsWindows.dirEntry.get(),
                    gui.SettingsWindows.intervalEntry.get())
        #return print(data)

        with open('config.yaml', 'w') as f:
            yaml.dump(data, f, allow_unicode=True)
        f.close
        
        return True

    def defineYamlFile(self, server, user, password, dir, interval):
        return {
            'server': server,
            'user': user,
            'password': password,
            'dir': dir,
            'interval': interval,
        }


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

    class HomeWindows:
        def __init__(self) -> None:
            self.window = Tk()
            self.window.title("RTSP Stream Capture")
            self.window.resizable(False, False)

            style = ttk.Style()
            style.configure('url.TEntry', padding=(10, 5))
            style.configure('capture.TButton', font=("Arial", 12, "bold"), padding=(0, 12))
            style.configure('icon.TButton', padding=5)

            windowFrame = ttk.Frame(self.window, padding=20)

            #url Box Frame
            urlFrame = ttk.Frame(windowFrame, borderwidth=1, relief='solid', padding=10)
            urlLabel = ttk.Label(urlFrame, text="Enter RTSP URL:", font=("Arial", 12, "bold"))
            urlText = ttk.Entry(urlFrame, width=80, style='url.TEntry')

            #mediaCanvas
            mediaFrame = ttk.Frame(windowFrame, padding=20)
            mediaCanvas = Canvas(mediaFrame, width=480, height=270, background='gray75')

            #ButtonsFrame
            buttonFrame = ttk.Frame(windowFrame)
            captureButton = ttk.Button(buttonFrame, text="START CAPTURE", width=52, style='capture.TButton')
            settingsIcon = PhotoImage(file='assets/settings.png')
            settingsButton = ttk.Button(buttonFrame, image=settingsIcon, width=5, style='icon.TButton')

            windowFrame.grid(column=0, row=0)

            urlFrame.grid(column=0, row=0, sticky=EW) #parent=>rootFrame
            urlLabel.grid(column=0, row=0, sticky=W)
            urlText.grid(column=0, row=1, columnspan=2, sticky=EW)

            mediaFrame.grid(column=0, row=1) #parent=>rootFrame
            mediaCanvas.grid(column=0, row=0, sticky=NSEW) #parent=>mediaFrame

            buttonFrame.grid(column=0, row=2, sticky=EW) #parent=>rootFrame
            captureButton.grid(column=0, row=0)
            settingsButton.grid(column=1, row=0)
    
            #Here check if server have been configured
            #self.Events(HomeWindows=self) .BeforeWindowsOpen()
            #self.window.mainloop()

        def call(self):
            gui.Events.BeforeWindowsOpen()
            gui.HomeWindows.draw()

        def draw(self):
            gui.HomeWindows.window.mainloop()

    class SettingsWindows:
        def __draw(self) -> None:
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
            #Add LineThrough

            self.serverFrame = ttk.Frame(self.windowFrame, padding=(0, 10))
            self.serverFrame.grid(column=0, row=1, sticky=W)
            self.serverLabel = ttk.Label(self.serverFrame, text="FTP Server:")
            self.serverEntry = ttk.Entry(self.serverFrame, width=40)
            self.serverLabel.grid(column=0, row=0, sticky=W)
            self.serverEntry.grid(column=0, row=1, sticky=W)
            #Add LineThrough

            self.userFrame = ttk.Frame(self.windowFrame, padding=(0, 0, 0, 10))
            self.userFrame.grid(column=0, row=2, sticky=W)
            self.userLabel = ttk.Label(self.userFrame, text="Username:")
            self.userEntry = ttk.Entry(self.userFrame, width=40)
            self.userLabel.grid(column=0, row=0, sticky=W)
            self.userEntry.grid(column=0, row=1, sticky=W)
            #Add LineThrough

            self.passwordFrame = ttk.Frame(self.windowFrame, padding=(0, 0, 0, 10))
            self.passwordFrame.grid(column=0, row=3, sticky=W)
            self.passwordLabel = ttk.Label(self.passwordFrame, text="Password:")
            self.passwordEntry = ttk.Entry(self.passwordFrame, width=40, show="*")
            self.passwordLabel.grid(column=0, row=0, sticky=W)
            self.passwordEntry.grid(column=0, row=1, sticky=W)
            #Add LineThrough

            self.dirFrame = ttk.Frame(self.windowFrame, padding=(0, 0, 0, 10))
            self.dirFrame.grid(column=0, row=4, sticky=W)
            self.dirLabel = ttk.Label(self.dirFrame, text="Directory Path")
            self.dirEntry = ttk.Entry(self.dirFrame, width=40)
            self.dirLabel.grid(column=0, row=0, sticky=W)
            self.dirEntry.grid(column=0, row=1, sticky=W)

            self.intervalFrame = ttk.Frame(self.windowFrame, padding=(0, 0, 0, 10))
            self.intervalFrame.grid(column=0, row=5, sticky=W)
            self.intervalLabel = ttk.Label(self.intervalFrame, text="Set Capture Intervals(sec):")
            self.intervalEntry = ttk.Entry(self.intervalFrame, width=22, validate="key")
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

        def show(self):
            gui.SettingsWindows.__draw()
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
            if gui.SettingsWindows.dirEntry.get() == '':
                messagebox.showinfo(message='Enter FTP server directory')
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

        def BeforeWindowsOpen(self):
            #print(f'FTP Server Check: {not script.checkFTPServerConfiguration()}')
            if not script.checkFTPServerConfiguration():
                gui.Events.OpenDialogForSettings()

        def OpenDialogForSettings(self):
            gui.SettingsWindows.show()

        def saveServerInformation(self):
            if gui.SettingsWindows.validateForm():
                script.updateConfigurationFile()
                messagebox.showinfo(message='Server Information updated!')
                gui.SettingsWindows.dismiss()

        def StartCapture(self):
            pass

script = Script()
gui = GUI()

def main():
    gui.HomeWindows.call()
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