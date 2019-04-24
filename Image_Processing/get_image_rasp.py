from picamera.array import PiRGBArray

class CapImage():
    def __init__(self,cap):
        self.cap = cap
        
    def get_image(self):
        raw=PiRGBArray(self.cap,size=(384,240))
        self.cap.capture(raw,format="bgr",resize=(384,240),use_video_port=True)
        return "",raw.array
