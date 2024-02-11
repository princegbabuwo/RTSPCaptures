from modules import RTSPScript

rtsp_url = None

def main():
    rtsp_url = ''
    ExecuteScript()

def ExecuteScript():
    RTSPScript(rtsp_url=rtsp_url)