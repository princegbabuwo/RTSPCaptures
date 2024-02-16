import time, cv2

class OpenStream:
    rtsp_url = None
    stream = None
    img_ext = '.jpg'

    def __init__(self, rtsp_url=rtsp_url, stream=stream) -> None:
        self.rtsp_url = rtsp_url
        self.stream =  self.__openStream()

    def __captureFrame(self):
        ret, frame = self.stream.read()
        if not ret:
            raise cv2.VideoCaptureException('Failed to read frame')
        return frame
    
    def __frametoImage(self, frame):
        captured, data = cv2.imencode(self.img_ext, frame)
        #print (f"Status: {captured} \nData2: {data}")
        #print (f"frame: {frame}")

        if not captured:
            raise ValueError("Image convertion failed")
        return data

    def __openStream(self):
        stream = cv2.VideoCapture(self.rtsp_url)
        if not stream.isOpened():
            raise IOError('Stream failed to open')
        return stream
    
    def __createFilename(self):
        return f"img_{time.time()}.jpg"

    def CaptureFrame(self):
        #This function will capture the frame, convert and return the converted file
        
        filename = self.__createFilename() #Create File Name
        frame = self.__captureFrame() #Capture frame
        return filename, frame, self.__frametoImage(frame) #convert and return frame
    
    def release(self):
        self.stream.release()