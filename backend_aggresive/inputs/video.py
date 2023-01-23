import time
import cv2
import imutils
from imutils.video import FPS
from imutils.video import VideoStream

class Video:
    """
    
    """
    def __init__(self, video_path):
        """
        
        """
        self.video_stream = cv2.VideoCapture(video_path)
        self.video_output = ('D:/Read Paper/Program/chicken_behaviour/results/output_video.mp4')
        self.writer = None
        self.W = None
        self.H = None
        
        self.fps = FPS().start()
        self.fr = 0
        
        self.totalFrames = 0
        self.time = time.time()
    
    def read_next_frame(self):
        """
        
        """
        frame = self.video_stream.read()
        frame = frame[1] if self.video_stream is None else frame

        if frame[1] is None:
            return False
        
        frame = imutils.resize(frame[1], width=1280, height=720)

        if self.W is None or self.H is None:
            (self.H, self.W) = frame.shape[:2]
            
        if self.video_output is not None and self.writer is None:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            self.writer = cv2.VideoWriter(self.video_output, fourcc, 15, (self.W, self.H))

        return dict({"total_frame" : self.totalFrames, "frame" : frame, "width" : self.W, 
        "height" : self.H})

    def write(self, frame):
        """
        
        """
        if self.writer is not None:
            self.writer.write(frame)

        self.totalFrames += 1
        self.fps.update()
    
    def stop(self):
        self.fps.stop()
        if self.writer is not None:
	        self.writer.release()
        self.video_stream.release()
    
    def get_video_stream(self):
        return self.video_stream
