import os, sys, time, traceback
from scripts import RTSP, FTP
from interface import GUI

def main():
    GUI.Homepage()

def script():
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