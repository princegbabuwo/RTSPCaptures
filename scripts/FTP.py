from ftplib import FTP

class Connect:
    ftp = None
    ftp_server = None
    ftp_user = None
    ftp_password = None 
    ftp_dir = None

    def __init__(self, ftp_server=ftp_server, ftp_user=ftp_user, 
                ftp_password=ftp_password, ftp_dir=ftp_dir) -> None:
        #initialize
        self.ftp_server = ftp_server
        self.ftp_user = ftp_user
        self.ftp_password = ftp_password
        self.ftp_dir = ftp_dir

        #Connect to FTP Server
        self.ftp = FTP(self.ftp_server)
        self.ftp.login(self.ftp_user, self.ftp_password)
        
        #Change dir
        if bool(self.ftp_dir): self.ftp.cwd(self.ftp_dir)
    
    def UploadImageData(self, file):
        self.ftp.storbinary(f"STOR {file}", open(file, 'rb'))
        return True

    def Close(self):
        #Close connections
        self.ftp.quit()
        
        