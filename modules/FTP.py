import time
from ftplib import FTP

class Connect:

    def __createFilename(self):
        return f"img_{time.time()}"
    
    def UploadImageData(self, image_data)
         with open(filename, "wb") as f:
            f.write(image_data.tobytes())
            ftp.storbinary(f"STOR {filename}", f)

    # 10. Close connections
    ftp.quit()
    cap.release()
        
        