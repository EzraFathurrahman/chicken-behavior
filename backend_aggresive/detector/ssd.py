import numpy as np
import pandas as pd
import time
from datetime import datetime
import cv2
import dlib
from imutils.video import VideoStream
from chicken_behaviour.tracker.centroidtracker import CentroidTracker
from chicken_behaviour.tracker.trackableobject import TrackableObject

class MobileNetSSD:
    """
    A class of pretrained MobileNetSSD to detect chicken.
    """

    def __init__(self, video):
        """
        Initialize the model by returning a pretrained model.
        """
        self.net = cv2.dnn.readNetFromCaffe('chicken_behaviour/detector/mobilenet_ssd/MobileNetSSD_deploy.prototxt', 'chicken_behaviour/detector/mobilenet_ssd/MobileNetSSD_deploy.caffemodel')
        self.video_stream = video.get_video_stream()
        self.trackers = []
        self.rects = []
        self.ct = CentroidTracker(maxDisappeared=1000, maxDistance=1000)
        self.trackableObjects = {}
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", 
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]
        self.tabular_output = []

    def detect(self, frame, W, H, skip_frames = 30, confidence = 0.4):
        """
        
        """
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()

        self.trackers = []
        self.rects = []

        for i in np.arange(0, detections.shape[2]):
            detection_proba = detections[0, 0, i, 2]
                
            if detection_proba > confidence:
                idx = int(detections[0, 0, i, 1])
                    
                if self.CLASSES[idx] != "bird":
                    continue
                box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                (startX, startY, endX, endY) = box.astype("int")
                tracks = self.initialize_tracker(frame, startX, startY, endX, endY)
                self.trackers.append(tracks)

    def initialize_tracker(self, frame, startX, startY, endX, endY):
        """
        
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        tracker = dlib.correlation_tracker()
        rect = dlib.rectangle(int(startX), int(startY), int(endX), int(endY))
        tracker.start_track(rgb, rect)
        
        return (tracker, rgb)
    
    def update_tracker_position(self):
        """
        
        """
        self.rects = []

        for tracker, rgb in self.trackers:
            tracker.update(rgb)
            pos = tracker.get_position()
            
            startX = int(pos.left())
            startY = int(pos.top())
            endX = int(pos.right())
            endY = int(pos.bottom())
            
            self.rects.append((startX, startY, endX, endY))

    def centroid_update(self, frame):
        """
        
        """
        self.objects = self.ct.update(self.rects)
        for (objectID, centroid) in self.objects.items():
            to = self.trackableObjects.get(objectID, None)

            if to is None:
                to = TrackableObject(objectID, centroid)
            else:
                y = [c[1] for c in to.centroids]
                direction = centroid[1] - np.mean(y)
                to.centroids.append(centroid)
            
            self.trackableObjects[objectID] = to

            text = "ID {}".format(objectID)
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
            
            self.write_tabular_output(objectID, centroid[0], centroid[1])

    def write_tabular_output(self, objectID, cX, cY):
        fps2 = self.video_stream.get(1)
        self.tabular_output.append([datetime.now(), time.process_time(), objectID, fps2, cX, cY])
    
    def save_output(self):
        data = pd.DataFrame(self.tabular_output)
        data.to_csv('D:/Read Paper/Program/chicken_behaviour/results/tabular_output.csv', index = False)
