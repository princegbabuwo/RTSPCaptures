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
    mediaLabel.grid(column=0, row=0, sticky=S, pady=10)

    buttonFrame.grid(column=0, row=2, sticky=EW) #parent=>rootFrame
    captureButton.grid(column=0, row=0)
    settingsButton.grid(column=1, row=0)

    window.mainloop()
    #return window, mediaImage, mediaLabel, captureButton

#CODE openStream
def openStream(url):
    #open stream
    stream = cv2.VideoCapture(url)
    if not stream.isOpened():
        raise IOError('Stream failed to open')
    return stream

#CODE captureFrame
def captureFrame(stream):
    #create filename 
    filename = f"img_{time.time()}.jpg"

    num_frames = stream.get(cv2.CAP_PROP_FRAME_COUNT)  # Get number of frames (estimate)
    return num_frames

    while True:
        if 0 < num_frames - 1:
            stream.set(cv2.CAP_PROP_POS_FRAMES, num_frames - 2)  # Seek to 2nd last frame
            stream.grab()  # Discard unwanted frame
        else:
            #capture frame
            ret, frame = stream.read()
            if not ret:
                raise cv2.VideoCaptureException('Failed to read frame')
            cv2.imshow('Frame', frame)
            
            #convert frame to Image Array
            captured, image = cv2.imencode('.jpg', frame)
            if not captured:
                raise ValueError("Image convertion failed")
            
            return filename, frame, image.tobytes()

#CODE uploadImageTOFTPServer
def uploadImageTOFTPServer():
    pass#ftp.storbinary(f"STOR {file}", open(file, 'rb'))

#CODE MainProcess
def MainProcess(window, captureButton, mediaImage, mediaLabel, rtsp_url, ftp_server, ftp_user, ftp_password, ftp_dir, interval):
    global _queue, thread_flag
    exc_type = None
    exc_obj = None
    exc_tb = None
    file_name = None
    line_number = None
    var_list = ('',)

    try:
        #with lock: mediaLabel.configure(text = '...Loading')

        #get stream
        if not thread_flag: raise Flag(var_list)
        stream = cv2.VideoCapture(rtsp_url)
        var_list = tuple(var_list) + ('stream',)
        if not thread_flag: raise Flag(var_list)
        if not stream.isOpened():
            raise IOError('Stream failed to open')
        fps = stream.get(cv2.CAP_PROP_FPS)
        print(stream)

        #Connect to ftp server
        ftp = ftplib.FTP(ftp_server)
        var_list = tuple(var_list) + ('ftp',)
        if not thread_flag: raise Flag(var_list)
        ftp.login(ftp_user, ftp_password)
        print(ftp)

        now = datetime.datetime.now()
        attempt = 0
        iterant = 0
        info = ''
        while thread_flag and attempt < 4:
            #the try statement here that handles errors wuthin the while statement as such errors can be retried
            try:
                stream.grab()
                if not thread_flag: raise Flag(var_list)
                frame_num = stream.get(cv2.CAP_PROP_POS_FRAMES)
                if not thread_flag: raise Flag(var_list)

                ret, frame = stream.retrieve()
                if not ret: raise cv2.VideoCaptureException('Failed to read frame')
                if not thread_flag: raise Flag(var_list)

                image = Image.fromarray(frame)
                print(f'image: {image}')
                picture = ImageTk.PhotoImage(image.resize((480, 270)))
                mediaImage.config(image=picture)
                mediaLabel.config(text=f'Frame Rate: {fps}fps\nBuffered Frame: {frame_num}; {info}')
                #print(frame_num)
                with lock:
                    if iterant == 0 or frame_num > iterant + (interval  * 10):

                        #convert frame to image
                        captured, image = cv2.imencode('.jpg', frame)
                        if not captured: raise ValueError("Image convertion failed")
                        if not thread_flag: raise Flag(var_list)
                        
                        #write image to machine
                        filename = f"img_{time.time()}.jpg"
                        with open(filename, "wb") as f:
                            f.write(image.tobytes())
                        f.close()
                        del f
                        if not thread_flag: raise Flag(var_list)

                        #upload image to ftp server
                        with open(filename, "rb") as f:
                            ftp.storbinary(f"STOR {filename}", f)
                        f.close()
                        if not thread_flag: raise Flag(var_list)
                        print ('Image uploaded successfully!')

                        #delete file from system and clear memory
                        os.remove(filename)
                        #del filename, frame, image, f, _image, picture 

                        attempt = 0
                        iterant = frame_num
                        info=f' Last Uploaded: frame {frame_num}'
            except Flag as t:
                raise Flag(var_list)
            except Exception as e:
                attempt += 1
                mediaLabel.configure(text=f'Error: {e}\nRetrying Process: {attempt} time(s)')
                if attempt > 2: 
                    mediaLabel.configure(text=f'Error: {e}\nNo more retries')
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
    #homeWindow, mediaLabel, mediaPlayer, captureButton = 
    HomeWindow()
    #print(homeWindow)
    #homeWindow.mainloop()



main()