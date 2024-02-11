import cv2
from ftplib import FTP

class RTSPScript:
    rtsp_url = None

    def __init__(self, rtsp_url=rtsp_url):
        self.rtsp_url = rtsp_url

    def OpenStream(self, rtsp_url):
        stream = cv2.VideoCapture(rtsp_url)
        if not stream.isOpened():
            raise IOError('Stream failed to open')
        return stream
    
    def CaptureFrame(self, stream):
        ret, frame = stream.read()
        if not ret:
            raise cv2.VideoCaptureException('Failed to read frame')
        return ret, frame
    
    def Execute(self):
        #1. Open Stream
        try:
            stream = self.OpenStream(self.rtsp_url)
        except Exception as e:
            return e
        
        #2. Once stream has successfully open wait 5secs before capture
