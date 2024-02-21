#This Application is written by Toye
#github.com/princegbabuwo
#email: princegbabuwo@gmail.com

#TODO Flag -> Image & Resources Clean up -> Clean up accrued image & resources when flag is raised
#TODO onWindowsClosed -> Image & Resources Clean up -> Clean up accrued image & resources when flag is raised

#CODE Imports
import time, datetime, cv2, queue, threading, os, sys, traceback, ftplib
from typing import final
from tkinter import *
#from ftplib import FTP
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

#CODE globals
thread_flag = True

#CODE Flag => Custom Error Manager
class Flag(Exception):
    def __init__(self, tuple_):
        self.tuple_ = tuple_  # 

    def __call__(self):
        return self.tuple_

#CODE HomeWindow
def HomeWindow():
    window = Tk()
    window.title("RTSP Stream Capture")
    window.resizable(False, False)
    #window.after(1, lambda: gui.Events.onWindowsOpen())

    style = ttk.Style()
    style.configure('url.TEntry', padding=(10, 5))
    style.configure('capture.TButton', font=("Arial", 12, "bold"), padding=(0, 12))
    style.configure('icon.TButton', padding=5)

    windowFrame = ttk.Frame(window, padding=20)

    #url Box Frame
    urlFrame = ttk.Frame(windowFrame, borderwidth=1, relief='solid', padding=10)
    urlLabel = ttk.Label(urlFrame, text="Enter RTSP URL:", font=("Arial", 12, "bold"))
    urlText = ttk.Entry(urlFrame, width=80, style='url.TEntry')

    #mediaCanvas
    mediaFrame = ttk.Frame(windowFrame, padding=20)
    mediaCanvas = Canvas(mediaFrame, width=480, height=270, background='gray75')
    mediaImage = ttk.Label(mediaFrame, background='gray75')
    mediaLabel = ttk.Label(mediaFrame)

    #ButtonsFrame
    buttonFrame = ttk.Frame(windowFrame)
    captureButton = ttk.Button(buttonFrame, text="START CAPTURE", width=52, style='capture.TButton', command=lambda: (onCaptureButtonClick(window, captureButton, mediaImage, mediaLabel)))
    settingsIcon = PhotoImage(file='assets/settings.png')
    settingsButton = ttk.Button(buttonFrame, image=settingsIcon, width=5, style='icon.TButton', command=lambda: print(0))

    #TK Grids
    windowFrame.grid(column=0, row=0)

    urlFrame.grid(column=0, row=0, sticky=EW) #parent=>rootFrame
    urlLabel.grid(column=0, row=0, sticky=W)
    urlText.grid(column=0, row=1, columnspan=2, sticky=EW)


    mediaFrame.grid(column=0, row=1) #parent=>rootFrame
    mediaCanvas.grid(column=0, row=0, sticky=NSEW) #parent=>mediaFrame
    mediaImage.grid(column=0, row=0, sticky=NSEW)
    mediaLabel.grid(column=0, row=0)

    buttonFrame.grid(column=0, row=2, sticky=EW) #parent=>rootFrame
    captureButton.grid(column=0, row=0)
    settingsButton.grid(column=1, row=0)

    window.mainloop()

#CODE MainProcess
def MainProcess(window, captureButton, mediaImage, mediaLabel, rtsp_url, ftp_server, ftp_user, ftp_password, ftp_dir, interval):
    global _queue, thread_flag
    exc_type = None
    exc_obj = None
    exc_tb = None
    file_name = None
    line_number = None
    attempt = 0
    var_list = ('',)

    try:
        mediaLabel.configure(text = '...Loading')

        #Open stream
        if not thread_flag: raise Flag(var_list)
        stream = cv2.VideoCapture(rtsp_url)
        var_list = tuple(var_list) + ('stream',)
        if not thread_flag: raise Flag(var_list)
        if not stream.isOpened():
            raise IOError('Stream failed to open')
        print(stream)

        #Connect to ftp server
        ftp = ftplib.FTP(ftp_server)
        var_list = tuple(var_list) + ('ftp',)
        if not thread_flag: raise Flag(var_list)
        ftp.login(ftp_user, ftp_password)

        now = datetime.datetime.now()
        while thread_flag:
            try:
                stream.grab() #Keep grabbing the frames as they buffer
                timesnap = datetime.datetime.now()
                if attempt > 0:  timesnap = now + datetime.timedelta(seconds=1)
                if not thread_flag: raise Flag(var_list)

                if now <= timesnap:
                    now = timesnap + datetime.timedelta(seconds=interval)
                    stream_props = stream.get(cv2.CAP_PROP_POS_FRAMES)

                    #Retrieved grabbed frame
                    filename = f"img_{time.time()}.jpg"
                    ret, frame = stream.retrieve()
                    if not ret: raise cv2.VideoCaptureException('Failed to retreive frame')
                    if not thread_flag: raise Flag(var_list)

                    #Upload frame to UI
                    image = Image.fromarray(frame)
                    picture = ImageTk.PhotoImage(image.resize((480, 270)))
                    mediaImage.config(image=picture)
                    mediaLabel.config(text=f'Frame Captured')

                    #convert frame to byteable image
                    captured, image = cv2.imencode('.jpg', frame)
                    if not captured: raise ValueError("Image convertion failed")
                    if not thread_flag: raise Flag(var_list)
                    
                    #write image to machine
                    with open(filename, "wb") as f:
                        f.write(image.tobytes())
                    f.close()
                    del f
                    if not thread_flag: raise Flag(var_list)

                    #raise IOError('Intentional Error')

                    #upload image to ftp server
                    with open(filename, "rb") as f:
                        ftp.storbinary(f"STOR {filename}", f) #I want to belive this function calls a continue
                    f.close()
                    if not thread_flag: raise Flag(var_list)
                    print ('Image uploaded successfully!')
                    mediaLabel.config(text='Frame Uploaded')

                    #delete file from system and clear memory
                    os.remove(filename)
                    #del filename, frame, image, f, _image, picture 

                    #Reset loop and if counters
                    attempt = 0
                    timesnap = datetime.datetime.now()
                    now = timesnap + datetime.timedelta(seconds=interval)
                    print (f'{timesnap}: Image Frame-{stream_props} Uploaded')
            except Flag as t:
                raise Flag(var_list)
            except Exception as e:
                attempt += 1
                hold = True
                mediaLabel.configure(text=f'Error: {e}\nRetrying Process: {attempt} time(s)')
                #if attempt > 3: mediaLabel.configure(text=f'Error: {e}\nNo more retries')
                time.sleep(2)
        else:
            raise Flag(var_list)
    except Flag as t:
        for e in t():
            if e == 'stream':
                stream.release()
            if e == 'ftp':
                ftp.close()
        mediaLabel.configure(text='PROCESS HALTED!!!')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        e = str(e)
        with lock:
            traceback.print_tb(exc_tb)
            print(f"Error:\n\tType: {exc_type}\n\tError: {e}")
            mediaLabel.config(text=f'Error: {e}')
    finally:
        #thread.join()
        thread_flag = True
        captureButton.configure(text='START CAPTURE', command=lambda: onCaptureButtonClick(window, captureButton, mediaImage, mediaLabel))


#CODE OnCaptureButtonClick
def onCaptureButtonClick(window, captureButton, mediaImage, mediaLabel):
    rtsp_url = 'http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg'
    ftp_server = 'ftp.dlptest.com'#'eu-central-1.sftpcloud.io'
    ftp_user = 'dlpuser'
    ftp_password = 'rNrKYTX9g7z3RgJRmxWuGHbeu'
    ftp_dir = ''
    interval = 10

    #ftp_server = 'eu-central-1.sftpcloud.io'
    #ftp_user = 'bada4bd30fa7453abdac3efaf11438b0'
    #ftp_password = 'GS6D5D19ahP8hg5jc52JtYDvpeQ00OWK'

    #switch to stop capture here
    captureButton.configure(text='STOP CAPTURE', command=lambda: stopCapture(mediaLabel))
        

    #set Thread parameters
    global lock, _queue, thread
    lock = threading.Lock()
    _queue = queue.Queue()
    #change Button state
    #use a thread
    #wait for the thread to complete execution then execute the thread below

    thread = threading.Thread(target=MainProcess, args=(window, captureButton, mediaImage, mediaLabel, rtsp_url, ftp_server, ftp_user, ftp_password, ftp_dir, interval), daemon=True)
    thread.start()

#CODE Stop Capture
def stopCapture(mediaLabel):
    global thread_flag
    thread_flag = False
    mediaLabel.configure(text='...Stopping')

#CODE main
def main():
    HomeWindow()


#if __name__ == 'main': 
main()