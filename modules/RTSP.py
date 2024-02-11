import cv2

class Initialize:
    rtsp_url = None
    img_ext = '.jpg'

    def __captureFrame(self, stream):
        ret, frame = stream.read()
        if not ret:
            raise cv2.VideoCaptureException('Failed to read frame')
        return frame
    
    def __frametoImage(self, frame):
         image_data, _ = cv2.imencode(self.img_ext, frame)
         return image_data

    def OpenStream(self, rtsp_url=rtsp_url):
        #print(rtsp_url)
        stream = cv2.VideoCapture(rtsp_url)
        if not stream.isOpened():
            raise IOError('Stream failed to open')
        return stream

    def CaptureFrame(self, stream):
        #This function will capture the frame, convert and return the converted file
        
        frame = self.__captureFrame(stream) #Capture frame
        return self.__frametoImage(frame) #convert and return frame