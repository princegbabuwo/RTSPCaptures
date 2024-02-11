import sys, time, traceback
from modules import RTSP

def main():
    rtsp_url = 'http://camera.buffalotrace.com/mjpg/video.mjpg'
    interval = 10
    try:
        rtsp = RTSP.Initialize()
        stream = rtsp.OpenStream(rtsp_url=rtsp_url) #initialize RTSP module paramenters
        #print(stream)

        #Capture Frame every 5 secs
        while True:
            ExecuteScript(rtsp, stream)
            time.sleep(interval)
    except Exception as e: #Here we want to capture the errors as much as possible
        ExceptionHandler(sys, e, 1)

def ExecuteScript(rtsp, stream):
    #print(rtsp)
    print (rtsp.CaptureFrame(stream))

def ExceptionHandler(sys, e, exit_code):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    traceback.print_tb(exc_tb)
    print(f"\nError: {str(e)}")
    sys.exit(exit_code)

main()