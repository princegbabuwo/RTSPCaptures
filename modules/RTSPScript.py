import cv2
from ftplib import FTP

class RTSPScript:
    rtsp_url = None
    img_ext = '.jpg'

    def __init__(self, rtsp_url=rtsp_url):
        self.rtsp_url = rtsp_url
        
        stream = self.OpenStream(self.rtsp_url) #Open Stream
        frame = self.CaptureFrame(stream) #Capture Frame
        return self.FrametoImage(frame)


    def OpenStream(self, rtsp_url):
        stream = cv2.VideoCapture(rtsp_url)
        if not stream.isOpened():
            raise IOError('Stream failed to open')
        return stream
    
    def CaptureFrame(self, stream):
        ret, frame = stream.read()
        if not ret:
            raise cv2.VideoCaptureException('Failed to read frame')
        return frame
    
    def FrametoImage(self, frame):
         image_data, _ = cv2.imencode(self.img_ext, frame)
         return image_data
